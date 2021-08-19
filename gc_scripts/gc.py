##
# Python program will run on selection.
##

# filename='/Users/lbusoni/Downloads/gc.py'
# exec(open(filename).read())

import numpy as np
import plotly
from plotly.graph_objs import Scatter, Layout
from gc_scripts.utils import get_temp_file, load_web_page


# Retrieve power and cadence
xx = np.asarray(GC.series(GC.SERIES_WATTS))
yy = np.asarray(GC.series(GC.SERIES_HRD))

temp_file = get_temp_file()

# Prepare Plot
plotly.offline.plot({
    "data": [Scatter(x=xx, y=yy, mode='markers')],
    "layout": Layout(title="Power / VAM")
}, auto_open=False, filename=temp_file.name)

# Load the webpage
load_web_page(GC, temp_file)
