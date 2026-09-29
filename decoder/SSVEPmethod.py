import numpy as np
from scipy import signal as scipysignal
from sklearn.cross_decomposition import CCA

class SSVEPmethod:
    def __init__(self, config):
        self.configs = config
        self.cca = CCA(n_components=1)
        
        self.samp_rate = self.configs["srate"]
        
        SSVEP_stim_freq = self.configs["freqs"]
        
        multiple_freq = 5
        
        templ_time = self.configs["flashTime"]
        
        self.templ_len = templ_time * (self.samp_rate)
        
        self.target_template_set = []
        
        samp_point = np.linspace(0, ((self.templ_len) - 1) / (self.samp_rate), int(self.templ_len), endpoint=True)
        
        samp_point = samp_point.reshape(1, len(samp_point))
        
        for freq in SSVEP_stim_freq:
            test_freq = np.linspace(freq, freq * multiple_freq, int(multiple_freq), endpoint=True)
            test_freq = test_freq.reshape(1, len(test_freq))
            num_matrix = 2 * (np.pi) * np.dot(test_freq.T, samp_point)
            cos_set = np.cos(num_matrix)
            sin_set = np.sin(num_matrix)
            cs_set = np.append(cos_set, sin_set, axis=0)
            self.target_template_set.append(cs_set)
    
    def recognize(self, data):
        p = []
        data = data.transpose()

        for template in self.target_template_set:
            template_T = template.T
            n_samples = data.shape[0]
            if n_samples <= template_T.shape[0]:
                template_aligned = template_T[-n_samples:, :]
            else:
                template_aligned = template_T
            self.cca.fit(data, template_aligned)
            data_tran, template_tran = self.cca.transform(data, template_aligned)
            rho = np.corrcoef(data_tran[:, 0], template_tran[:, 0])[0, 1]
            p.append(rho)
        result = p.index(max(p))
        return {"result": result, "raw": p}
    
    def pre_filter(self, data):
        fs = (self.samp_rate) / 2
        N, Wn = scipysignal.ellipord([6 / fs, 30 / fs], [2 / fs, 40 / fs], 3, 40)
        b1, a1 = scipysignal.ellip(N, 1, 45, Wn, "bandpass")
        filter_data = scipysignal.filtfilt(b1, a1, data)
        return filter_data
