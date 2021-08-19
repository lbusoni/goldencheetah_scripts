# This chart plots for every USER interval the average power the athlete
# has produced
import bisect
import plotly
import plotly.graph_objs as go
import numpy as np
from gc_scripts.utils import get_temp_file, load_web_page

# Get activity (used to get the date)
activity = GC.activityMetrics()

# Get zone information at this actvity date
zone = GC.athleteZones(date=activity["date"], sport="bike")

# Get intervals USER if that one is not find get all intervals
#intervals = GC.activityIntervals(type="UTILIZZATORE")
intervals = GC.activityIntervals()
type_title = "USER"

temp_file = get_temp_file()


# Define GC background color
gc_bg_color = 'rgb(52,52,52)'
# Define GC Text color
gc_text_color = 'rgb(255,255,255)'

valid_intervals = np.nonzero(intervals['selected'])[0]

# if intervals["name"]:
if len(valid_intervals) > 0:
    # Identify for every interval the zone color
    breaks = zone["zoneslow"][0]
    zone_colors = zone["zonescolor"][0]
    interval_colors = []
    avg_power_pct = []
    for idx in range(len(intervals["selected"])):
        if intervals["selected"][idx]:
            interval = intervals["Average_Power"][idx]
            id = bisect.bisect_left(breaks, interval)
            interval_colors.append(zone_colors[id - 1])
            avg_power_pct.append(
                str(round((interval / zone["cp"][0]) * 100, 1)) + "%")

    # Define chart title
    title = "Average Power per Interval (CP:" + str(
        zone["cp"][0]) + ") Interval Type=" + str(type_title)

    # Add percentage labels
    zone_names = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]
    legend = []
    zone_index = 1
    for zone in breaks:
        legend.append("Z" + str(zone_index) + "(" + str(zone) + ")")
        zone_index += 1

    # array of lap names to printed on the x-axis
    lap_names = np.asarray(intervals["name"])[valid_intervals]
    # array of y values
    watts_y = np.asarray(intervals["Average_Power"])[valid_intervals]
    # define x-axis (start time of the intervals)
    x = np.asarray(intervals["start"])[valid_intervals]

    # arrays used for text for every interval
    duration = np.asarray(intervals["Duration"])[valid_intervals]
    distance = np.asarray(intervals["Distance"])[valid_intervals]

    trace0 = go.Scatter(
        x=x,
        y=watts_y,
        mode='text',
        showlegend=False,
    )

    data = [trace0]

    # workaround to get a custom legend
    for i in np.arange(0, len(legend)):
        data.append(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, color=zone_colors[i]),
            legendgroup=legend[i],
            showlegend=True,
            name=legend[i],
        )
        )

    # Create rectangles per interval
    shapes = []
    annotations = []
    x_label_pos = []

    for i in np.arange(0, len(lap_names)):
        x_label_pos.append(x[i] + (duration[i] / 2))

        shapes.append(
            {
                'type': 'rect',
                'x0': x[i],
                'y0': 0,
                'x1': x[i] + duration[i],
                'y1': watts_y[i],
                'fillcolor': interval_colors[i],
            })

        m, s = divmod(duration[i], 60)
        h, m = divmod(m, 60)
        if h > 0:
            duration_formatted = str(int(h)) + "h" + \
                str(int(m)) + "m" + str(int(s)) + "s"
        elif m > 0:
            duration_formatted = str(int(m)) + "m" + str(int(s)) + "s"
        else:
            duration_formatted = str(int(s)) + "s"
        annotations.append(
            dict(
                x=x[i] + (duration[i] / 2),
                y=watts_y[i],
                xref='x',
                yref='y',
                text=str(avg_power_pct[i]) + "<br>" + duration_formatted +
                "<br>" + str(round(distance[i], 2)) + "km",
                showarrow=True,
                arrowhead=7,
                arrowcolor=gc_text_color,
                ax=0,
                ay=-40,
                font=dict(
                    color=gc_text_color,
                    size=12
                ),
            )
        )
    # end for

    layout = go.Layout(
        title=title,
        paper_bgcolor=gc_bg_color,
        plot_bgcolor=gc_bg_color,
        font=dict(
            color=gc_text_color,
            size=12
        ),
        xaxis=dict(
            tickvals=x_label_pos,
            ticktext=lap_names,
            tickangle=45,
            showgrid=True,
            rangemode='nonnegative',
        ),
        yaxis=dict(
            range=[0,  max(watts_y) + 100],
            nticks=int(max(watts_y) / 10),
            ticks='outside',
            showgrid=True,
            zeroline=True,
            showline=True,
            gridcolor="grey",
            title="Watts",
        ),
        margin=go.layout.Margin(
            l=100,
            r=0,
            b=100,
            t=150,
            pad=0
        ),
        shapes=shapes,
        annotations=annotations,
    )

    fig = go.Figure(data=data, layout=layout)
    plot = plotly.offline.plot(fig, auto_open=False, filename=temp_file.name)
else:
    f = open(temp_file.name, "w+")
    lines_of_text = [
        "<html>",
        "<body>",
        "<p> Unable to draw plot <br> Please select intervals from the Side bar </p>",
        "</body>",
        "</html>"
    ]
    f.writelines(lines_of_text)
    f.close()

# Load the webpage
load_web_page(GC, temp_file)
