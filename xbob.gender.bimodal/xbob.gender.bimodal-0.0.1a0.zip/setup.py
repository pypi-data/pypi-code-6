#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch> 
# Mon Apr  7 23:06:06 CEST 2014
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

setup(

    name='xbob.gender.bimodal',
    version='0.0.1a0',
    description='Bimodal gender recognition',

    url='http://pypi.python.org/pypi/xbob.gender.bimodal',
    license='GPLv3',
    author='Laurent El Shafey',
    author_email='laurent.el-shafey@idiap.ch',
    keywords='bob, xbob, gender recognition, face, speech, bimodal',

    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,

    # This line defines which packages should be installed when you "install"
    # this package. All packages that are mentioned here, but are not installed
    # on the current system will be installed locally and only visible to the
    # scripts of this package. Don't worry - You won't need adminstrative
    # privileges when using buildout.
    install_requires=[
      'setuptools',
      'bob == 1.2.2', # base signal proc./machine learning library
      'xbob.db.verification.filelist',
      'facereclib == 1.2.1',
      'bob.spear == 1.1.2',
    ],

    namespace_packages = [
      'xbob',
      'xbob.gender',
    ],

    # This entry defines which scripts you will have inside the 'bin' directory
    # once you install the package (or run 'bin/buildout'). The order of each
    # entry under 'console_scripts' is like this:
    #   script-name-at-bin-directory = module.at.your.library:function
    #
   entry_points={

      # scripts should be declared using this entry:
      'console_scripts': [
        'cosine_distance.py = xbob.gender.bimodal.script.cosine_distance:main',
        'gmm_training.py = xbob.gender.bimodal.script.gmm_training:main',
        'para_gmm_training.py = xbob.gender.bimodal.script.para_gmm_training:main',
        'gmm_scoring.py = xbob.gender.bimodal.script.gmm_scoring:main',
        'isv_training.py = xbob.gender.bimodal.script.isv_training:main',
        'isv_scoring.py = xbob.gender.bimodal.script.isv_scoring:main',
        'ivector.py = xbob.gender.bimodal.script.ivector:main',
        'para_ivector.py = xbob.gender.bimodal.script.para_ivector:main',
        'mfcc_vad_energy.py = xbob.gender.bimodal.script.mfcc_vad_energy:main',
        'svm.py = xbob.gender.bimodal.script.svm:main',
        'svm_linear.py = xbob.gender.bimodal.script.svm_linear:main',

        'fusion_mobio.py = xbob.gender.bimodal.script.fusion_mobio:main',

        'plot_feret.py = xbob.gender.bimodal.script.plot_feret:main',
        'plot_lfw.py = xbob.gender.bimodal.script.plot_lfw:main',
        'plot_mobio.py = xbob.gender.bimodal.script.plot_mobio:main',
        'plot_nistsre.py = xbob.gender.bimodal.script.plot_nistsre:main',
       ],

      'facereclib.database': [
        'gferet = xbob.gender.bimodal.configurations.databases.feret:database',
        'gferet-female = xbob.gender.bimodal.configurations.databases.feret:database_female',
        'gferet-male = xbob.gender.bimodal.configurations.databases.feret:database_male',

        'glfw-fold0 = xbob.gender.bimodal.configurations.databases.lfw_fold0:database',
        'glfw-fold0-female = xbob.gender.bimodal.configurations.databases.lfw_fold0:database_female',
        'glfw-fold0-male = xbob.gender.bimodal.configurations.databases.lfw_fold0:database_male',
        'glfw-fold1 = xbob.gender.bimodal.configurations.databases.lfw_fold1:database',
        'glfw-fold1-female = xbob.gender.bimodal.configurations.databases.lfw_fold1:database_female',
        'glfw-fold1-male = xbob.gender.bimodal.configurations.databases.lfw_fold1:database_male',
        'glfw-fold2 = xbob.gender.bimodal.configurations.databases.lfw_fold2:database',
        'glfw-fold2-female = xbob.gender.bimodal.configurations.databases.lfw_fold2:database_female',
        'glfw-fold2-male = xbob.gender.bimodal.configurations.databases.lfw_fold2:database_male',
        'glfw-fold3 = xbob.gender.bimodal.configurations.databases.lfw_fold3:database',
        'glfw-fold3-female = xbob.gender.bimodal.configurations.databases.lfw_fold3:database_female',
        'glfw-fold3-male = xbob.gender.bimodal.configurations.databases.lfw_fold3:database_male',
        'glfw-fold4 = xbob.gender.bimodal.configurations.databases.lfw_fold4:database',
        'glfw-fold4-female = xbob.gender.bimodal.configurations.databases.lfw_fold4:database_female',
        'glfw-fold4-male = xbob.gender.bimodal.configurations.databases.lfw_fold4:database_male',

        'gmobio = xbob.gender.bimodal.configurations.databases.mobio:database',
        'gmobio-female = xbob.gender.bimodal.configurations.databases.mobio:database_female',
        'gmobio-male = xbob.gender.bimodal.configurations.databases.mobio:database_male',

        'gnistsre = xbob.gender.bimodal.configurations.databases.nistsre:database',
        'gnistsre-female = xbob.gender.bimodal.configurations.databases.nistsre:database_female',
        'gnistsre-male = xbob.gender.bimodal.configurations.databases.nistsre:database_male',
      ],

      'facereclib.preprocessor': [
        'face-crop-16 = xbob.gender.bimodal.configurations.preprocessing.face_crop_16:preprocessor',
        'face-crop-24 = xbob.gender.bimodal.configurations.preprocessing.face_crop_24:preprocessor',
        'face-crop-32 = xbob.gender.bimodal.configurations.preprocessing.face_crop_32:preprocessor',
        'face-crop-48 = xbob.gender.bimodal.configurations.preprocessing.face_crop_48:preprocessor',
        'face-crop-64 = xbob.gender.bimodal.configurations.preprocessing.face_crop_64:preprocessor',
        'face-crop-80 = xbob.gender.bimodal.configurations.preprocessing.face_crop_80:preprocessor',
      ],

      'facereclib.feature_extractor': [
        'hog-16 = xbob.gender.bimodal.configurations.features.hog_16:feature_extractor',
        'hog-24 = xbob.gender.bimodal.configurations.features.hog_24:feature_extractor',
        'hog-32 = xbob.gender.bimodal.configurations.features.hog_32:feature_extractor',
        'hog-48 = xbob.gender.bimodal.configurations.features.hog_48:feature_extractor',
        'hog-64 = xbob.gender.bimodal.configurations.features.hog_64:feature_extractor',
        'hog-80 = xbob.gender.bimodal.configurations.features.hog_80:feature_extractor',
        'lbphs = xbob.gender.bimodal.configurations.features.lbphs:feature_extractor',
      ],

      'facereclib.tool': [
        'mygmm = xbob.gender.bimodal.configurations.tools.gmm:tool',
        'myisv = xbob.gender.bimodal.configurations.tools.isv:tool',
        'myivector = xbob.gender.bimodal.configurations.tools.ivector:tool',
        'myivector200 = xbob.gender.bimodal.configurations.tools.ivector200:tool',
        'cosine = xbob.gender.bimodal.configurations.tools.cosine:tool',
      ],

    },

    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
