import os
from libs.iRunnerPlugin import IRunnerPlugin
from xml.dom.minidom import parse

class BehatPlugin(IRunnerPlugin):

    fileResult = ''

    def activate(self):
        super(BehatPlugin, self).activate()
        return "Behat plugin actif"

    def deactivate(self):
        super(BehatPlugin, self).deactivate()
        return "Behat plugin inactif"

    def getFileResult(self, script):
        return script.split('/')[-1].split('.')[0]

    def run(self, profile, script):
        behat='behat --profile %s  --format=junit --out=./result/%s/ features/%s' % (profile,profile,script)
        return os.system(behat)

    def result(self, profile, script):
        fileResult = self.getFileResult(script)
        resultFinal = ''
        testCaseList=[]
        notes=''
        try:
            resultxml = parse('result/%s/TEST-%s.xml' % (profile, fileResult))
            testCaseList = resultxml.getElementsByTagName('testcase')
            error = resultxml.getElementsByTagName('testsuite')[0].getAttribute('errors')
            failure = resultxml.getElementsByTagName('testsuite')[0].getAttribute('failures')
            notes = notes + resultxml.getElementsByTagName('testsuite')[0].getAttribute('name')+'\n'
        except Exception as e:
            error = 0
            failure = 1
            notes = 'Tests sous %s non passe' % profile
        if error == '0' and failure == '0':
            resultFinal = 'p'
        else:
            resultFinal = 'f'
        for testcase in testCaseList:
            notes = notes+testcase.getAttribute('name')+'\n   Temps execution : %s' % testcase.getAttribute('time')+'\n'
            failuresList = testcase.getElementsByTagName('failure')
            for failure in failuresList:
                notes = notes + '      Erreur : '+failure.getAttribute('message')+'\n'
        notes = notes + '\n'
        return (resultFinal, notes)





