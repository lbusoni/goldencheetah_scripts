##
## Python program will run on selection.
##

# filename='/Users/lbusoni/Downloads/gc.py'
# exec(open(filename).read())

import numpy as np
import plotly
from plotly.graph_objs import Scatter, Layout
import tempfile
import pathlib


## Retrieve power and cadence
xx = np.asarray(GC.series(GC.SERIES_WATTS))
yy = np.asarray(GC.series(GC.SERIES_HRD))

# Define temporary file
temp_file = tempfile.NamedTemporaryFile(mode="w+t", prefix="GC_", suffix=".html", delete=False)

## Prepare Plot
plotly.offline.plot({
    "data": [Scatter(x=xx, y=yy, mode = 'markers')],
    "layout": Layout(title="Power / VAM")
}, auto_open = False, filename=temp_file.name)

## Load Plot
GC.webpage(pathlib.Path(temp_file.name).as_uri())


