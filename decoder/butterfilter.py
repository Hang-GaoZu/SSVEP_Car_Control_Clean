"""用于在绘图前对EEG数据进行滤波"""

from scipy import signal
import numpy as np

class ButterFilter:
    def __init__(self):
        pass

    def reset(self, srate=250, chs=8, fltparam=None, eegtype="float32"):
        if fltparam is None:
            fltparam = [(49, 51), (0.5, 45), (1, 0)]
        self.srate = srate
        self.chs = chs
        self.fltparam = fltparam
        self.padL = int(self.srate)
        self.cache = np.zeros((self.chs, self.padL), dtype=eegtype)

        self.rawdata = None
        self.ndata = None
        self.bdata = None
        self.hdata = None
        self._genFilters()

    def _genFilters(self):
        fs = self.srate / 2.0
        self.nflt = signal.butter(N=2, Wn=[self.fltparam[0][0] / fs, self.fltparam[0][1] / fs], btype="stop")
        self.hflt = signal.butter(N=2, Wn=self.fltparam[2][0] / fs, btype="highpass")
        self.bflt = signal.butter(N=2, Wn=[self.fltparam[1][0] / fs, self.fltparam[1][1] / fs], btype="bandpass")

    def update(self, fdat):
        if self.cache is None:
            return False
        r, c = fdat.shape
        self.cache = np.hstack((self.cache, fdat))
        dat = self.cache.copy()
        self.ndata = signal.lfilter(self.nflt[0], self.nflt[1], dat)
        self.hdata = signal.lfilter(self.hflt[0], self.hflt[1], self.ndata)
        self.bdata = signal.lfilter(self.bflt[0], self.bflt[1], self.ndata)

        self.rawdata = self.cache[:, -c:]
        self.ndata = self.ndata[:, -c:]
        self.hdata = self.hdata[:, -c:]
        self.bdata = self.bdata[:, -c:]

        self.cache = self.cache[:, -self.padL:]
        return True


class FirFilter:
    def __init__(self):
        pass

    def reset(self, srate=250, chs=8, fltparam=None, eegtype="float32"):
        if fltparam is None:
            fltparam = [(49, 51), (0.5, 45)]
        self.srate = srate
        self.chs = chs
        self.fltparam = fltparam
        self.padL = int(self.srate * 8)
        self.cache = np.zeros((self.chs, self.padL), dtype=eegtype)

        self.rawdata = None
        self.ndata = None
        self.bdata = None
        self.hdata = None
        self._genFilters()

    def _genFilters(self):
        fs = self.srate / 2.0
        nb = signal.firwin(int(self.srate) * 3 + 1, [self.fltparam[0][0] / fs, self.fltparam[0][1] / fs], pass_zero="bandstop")
        self.nflt = [nb, 1]
        fb = signal.firwin(int(self.srate) * 4 + 1, [self.fltparam[1][0] / fs, self.fltparam[1][1] / fs], pass_zero="bandpass")
        self.bflt = [fb, 1]

    def update(self, fdat):
        if self.cache is None:
            return False
        r, c = fdat.shape
        self.cache = np.hstack((self.cache, fdat))
        dat = self.cache.copy()
        self.ndata = signal.lfilter(self.nflt[0], self.nflt[1], dat)
        self.bdata = signal.lfilter(self.bflt[0], self.bflt[1], dat)

        self.rawdata = self.cache[:, -c:]
        self.ndata = self.ndata[:, -c:]
        self.bdata = self.bdata[:, -c:]

        self.cache = self.cache[:, -self.padL:]
        return True