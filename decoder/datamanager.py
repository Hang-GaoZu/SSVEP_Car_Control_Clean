import numpy as np

class DataManager:
    def __init__(self):
        self.data = None

    def config(self, srate, chs, period, eegtype):
        self.dmL = srate * period
        self.chs = chs
        self.data = np.zeros((self.chs, self.dmL), dtype=eegtype)
        self.packcache = np.zeros((self.chs, 1))
        self.pack = None
        self.ptr = 0
        self.updateCof = int(0.05 * srate)

    def update(self, pack):
        self.packcache = np.hstack((self.packcache, pack))
        r, c = self.packcache.shape
        if c < self.updateCof:
            return 0
        self._update(self.packcache[:, 1:])
        self.packcache = np.zeros((self.chs, 1))
        return 1

    def _update(self, pack):
        r, c = pack.shape
        sp = self.dmL - self.ptr

        if sp > c:
            self.data[:, self.ptr:self.ptr + c] = pack
            self.ptr += c
        elif sp == c:
            self.data[:, self.ptr:self.ptr + c] = pack
            self.ptr = 0
        else:
            self.data[:, self.ptr:self.ptr + sp] = pack[:, :sp]
            self.data[:, 0:c - sp] = pack[:, sp:]
            self.ptr = c - sp
        return 1

if __name__ == "__main__":
    dm = DataManager()
    dm.config(40, 1, 4, 55)
    s = 0
    for i in range(200):
        pack = np.arange(s, s + 5)
        s += 5
        pack = pack[np.newaxis, :]
        if dm.update(pack):
            print(dm.data[0, :])