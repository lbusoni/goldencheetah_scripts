# This chart export activity series in pandas format
import pandas as pd
import datetime

act = GC.activity()
dd = {}
for k,v in act.items():
    dd[k] = np.array(v)
df = pd.DataFrame(dd)
data = GC.activityMetrics()['date']
ora = GC.activityMetrics()['time']
dt = datetime.datetime.combine(data,ora)
timestamp = dt.strftime("%Y%m%d_%H%M%S")
filename="/Users/lbusoni/Downloads/GC_export_%s.csv" % timestamp
df.to_csv(filename)
print(filename)
print("restore with df=pd.read_csv(%s)" % filename)
