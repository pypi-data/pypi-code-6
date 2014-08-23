from photoz import PhotoSample # import the library
import numpy as np

import os
import photoz as phz

# Instantiate the class
UserCatalogue = PhotoSample(filename="PHAT0", family="Gamma", link="log")

# Make a training size array to loop through
train_size_arr = np.arange(500,10000,500)
catastrophic_error = []

# Select your number of components
UserCatalogue.num_components = 4

for i in range(len(train_size_arr)):
    UserCatalogue.do_PCA()

    UserCatalogue.test_size = train_size_arr[i]

    UserCatalogue.split_sample(random=True)
    UserCatalogue.do_GLM()

catastrophic_error.append(UserCatalogue.catastrophic_error)

min_indx = np.array(catastrophic_error) < 0.01
optimimum_train_size = train_size_arr[min_indx]
