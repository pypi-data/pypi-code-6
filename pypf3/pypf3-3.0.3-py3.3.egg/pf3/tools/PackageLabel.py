
import logging
import traceback
import subprocess

COMMASPACE = ', '

class PackageLabel():

    fop_exec = None
    fop_config = None
    noosh_monitor = None

    def __init__(self,fop_exec, fop_config, noosh_monitor):
        self.logger = logging.getLogger('pf3')
        self.fop_exec = fop_exec
        self.fop_config = fop_config
        self.noosh_monitor = noosh_monitor

    def generate(self, fo_file, specification):
        self.logger.info('Generating package lable for PIC Cde: '+ specification['reference_number'])

        try:
            cmd = ['"'+self.fop_exec+'"', '-c='+self.fop_config,
                   '"'+specification['reference_number']+'"']
            cmd_str = ' '.join(cmd)
            p = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processResult = p.communicate()
        except subprocess.CalledProcessError:
                # check return status to see what pdftoolbox thinks
                self.logger.error('Problem calling command: '+str(cmd))
                self.logger(traceback.format_exc())

