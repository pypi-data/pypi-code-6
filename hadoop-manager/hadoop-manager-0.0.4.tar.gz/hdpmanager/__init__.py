"""
        hadoop-manager
        ~~~~~~~~~~~~~~

        Python wrapper around Hadoop streaming jar.
"""

__author__ = 'Jure Ham <jure.ham@zemanta.com>'

__all__ = ['HadoopManager', 'HadoopCmdPromise', 'HadoopJob', 'HadoopFs', 'Mapper', 'Reducer', 'Combiner']


from hdpmanager import HadoopManager, HadoopCmdPromise

from hdpjob import HadoopJob
from hdpfs import HadoopFs

from mapper import Mapper
from reducer import Reducer
from combiner import Combiner
