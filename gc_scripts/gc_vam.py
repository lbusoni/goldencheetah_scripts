import plotly
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
import numpy as np
from gc_scripts.utils import get_temp_file, load_web_page
import pandas as pd

roll_period = 30

time = np.asarray(GC.series(GC.SERIES_SECS))
cad = np.asarray(GC.series(GC.SERIES_CAD))
power_raw = np.asarray(GC.series(GC.SERIES_WATTS))
slope_raw = np.asarray(GC.series(GC.SERIES_SLOPE))
speed_raw = np.asarray(GC.series(GC.SERIES_KPH))

power = pd.Series(power_raw, time).rolling(roll_period, center=True).mean()
slope = pd.Series(slope_raw, time).rolling(roll_period, center=True).mean()
speed = pd.Series(speed_raw, time).rolling(roll_period, center=True).mean()
vam = 1e3 * speed * np.sin(np.arctan(slope / 100))

valid_vam = vam > 0
valid_speed = speed < 25
valid_cad = cad > 0
valid = valid_vam & valid_speed & valid_cad

power_valid = power[valid]
vam_valid = vam[valid]


temp_file = get_temp_file()
# Define GC background color
gc_bg_color = 'rgb(52,52,52)'
# Define GC Text color
gc_text_color = 'rgb(255,255,255)'

layout = go.Layout(
    title="VAM vs Power",
    paper_bgcolor=gc_bg_color,
    plot_bgcolor=gc_bg_color,
    font=dict(
        color=gc_text_color,
        size=12
    ),
    yaxis=dict(
        tickangle=45,
        showgrid=True,
        rangemode='nonnegative',
        title="VAM [m/h]"
    ),
    xaxis=dict(
        range=[0, max(power_valid) + 100],
        nticks=int(max(power_valid) / 10),
        ticks='outside',
        showgrid=True,
        zeroline=True,
        showline=True,
        gridcolor="grey",
        title="Power [W]",
    ),
    margin=go.layout.Margin(
        l=100,
        r=0,
        b=100,
        t=150,
        pad=0
    ),
)


# Prepare Plot
plotly.offline.plot({
    "data": [Scatter(x=power_valid, y=vam_valid, mode='markers')],
    "layout": layout
}, auto_open=False, filename=temp_file.name)

# Load the webpage
load_web_page(GC, temp_file)
