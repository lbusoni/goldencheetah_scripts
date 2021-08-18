import pandas as pd
import numpy as np
import os
from gc_scripts.package_data import data_root_dir


class CompareStravaPower():

    def __init__(self, file1, file2):
        self._df1 = pd.read_csv(file1)
        self._df2 = pd.read_csv(file2)
        self._delay = self.estimate_delay(self._df1, self._df2)

    @staticmethod
    def estimate_delay(df1, df2):
        # estimate time delay by correlation
        lags = range(-1000, 1000)
        rs = [df1['altitude'].corr(df2['altitude'].shift(lag)) for lag in lags]
        delayAlt = lags[np.argmax(rs)]
        rs = [df1['latitude'].corr(df2['latitude'].shift(lag)) for lag in lags]
        delayLat = lags[np.argmax(rs)]
        rs = [df1['longitude'].corr(df2['longitude'].shift(lag))
              for lag in lags]
        delayLon = lags[np.argmax(rs)]
        rs = [df1['power'].corr(df2['power'].shift(lag))
              for lag in lags]
        delayPow = lags[np.argmax(rs)]
        print("delays %d %d %d %d" % (delayAlt, delayLat, delayLon, delayPow))
        return delayLat

    def errAltitude(self):
        return self._error('altitude')

    def errLatitude(self):
        return self._error('latitude')

    def errLongitude(self):
        return self._error('longitude')

    def errPower(self):
        return self._error_rolling('power', roll=10)

    def _error(self, what):
        return self._df1[what] - self._df2[what].shift(self._delay)

    def _error_rolling(self, what, roll=10):
        return self._df1[what].rolling(roll, center=True).mean() - \
            self._df2[what].shift(self._delay).rolling(
                roll, center=True).mean()

    def plotP(self, roll=50):
        self._df1['power'].rolling(roll, center=True).mean().plot()
        self._df2['power'].shift(self._delay).rolling(
            roll, center=True).mean().plot()


def main():
    # karoo
    file1 = os.path.join(data_root_dir(), 'GC_export_20210816_181909.csv')
    # strava
    file2 = os.path.join(data_root_dir(), 'GC_export_20210816_181532.csv')
    csp = CompareStravaPower(file1, file2)
    return csp
