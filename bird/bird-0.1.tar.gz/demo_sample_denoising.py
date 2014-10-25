# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Manuel Moussallam <manuel.moussallam@gmail.com>
#
# License: BSD (3-clause)

import numpy as np
from bird import bird, s_bird
from joblib import Memory
import mne
from mne.datasets import sample

data_path = sample.data_path()

scales = [8, 16, 32, 64]
n_runs = 20

# Structured sparsity parameters
l = 1.0

ave_fname = data_path + '/MEG/sample/sample_audvis-no-filter-ave.fif'
# evoked = mne.read_evokeds(ave_fname, condition=0, baseline=None)
evoked = mne.read_evokeds(ave_fname, condition=3, baseline=(-0.2, None))
evoked = mne.pick_types_evoked(evoked, meg='grad', eeg=False)

data = 1e13 * evoked.data

data = data[np.argsort(np.max(np.abs(data), axis=1))[-40:]]

n_jobs = -1
memory = Memory(cachedir='/tmp')
random_state = 42
max_iter = 100
p_above = 1e-6

bird_estimate = bird(data, scales, n_runs, p_above=p_above,
                     max_iter=max_iter, random_state=random_state,
                     n_jobs=n_jobs, memory=memory)
sbird_estimate = s_bird(data, scales, n_runs, p_above=p_above,
                        p_active=l, max_iter=max_iter,
                        random_state=random_state,
                        n_jobs=n_jobs, memory=memory)

times = 1e3 * evoked.times

subsample = 20

import matplotlib.pyplot as plt
plt.figure(figsize=(7, 5))
p1 = plt.plot(times, data[:subsample].T, 'k', alpha=0.3)
p2 = plt.plot(times, bird_estimate[:subsample].T, 'r-', linewidth=1.5)
p3 = plt.plot(times, sbird_estimate[:subsample].T, 'g-', linewidth=1.5)

plt.legend((p1[0], p2[0], p3[0]),
           ('Data', 'BIRD Estimates', 'S-BIRD Estimates'),
           loc='upper right')

plt.xlabel('Time (ms)', fontsize=16.0)
plt.ylabel('MEG')
plt.show()
