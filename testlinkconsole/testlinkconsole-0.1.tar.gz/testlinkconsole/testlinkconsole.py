import ConfigParser
import os
import sys
import datetime
import string
import logging
#from testlink import TestlinkAPIClient, TestLinkHelper
from termcolor import colored
from progressbar import ProgressBar, Bar
from yapsy.PluginManager import PluginManagerSingleton
from libs.iRunnerPlugin import IRunnerPlugin
from libs.iBDTestPlugin import IBDTestPlugin
from libs.consoleBase import ConsoleBase


class TestLinkConsole(ConsoleBase):

    prompt = colored('testlink : ','green')
    intro = colored('Testlink Console client','grey')
    section = 'testlink'
    configFile = 'testlinkclient.cfg'
    logger = 0

    projetid = 0
    campagneid = 0
    serverUrl = ''
    serverKey = ''
    apiclient = ''
    output = False
    runner = ''
    plugins = ''

    LIST_OBJECTS = [ 'projets', 'campagnes', 'tests']
    LIST_VARIABLE = { 
            'projetid'   : 'ID projet', 
            'campagneid' : 'ID campagne',
            'serverUrl'  : 'Url du serveur testlink',
            'serverKey'  : 'API Key du server',
            'output'     : 'Output',
            'runner'     : 'test runner (plugin : behat, behave ...)',
            }

    def __init__(self, config, logger):
        ConsoleBase.__init__(self,config) 
        self.logger = logger
        self.plugins = PluginManagerSingleton.get()
        self.plugins.app = self
        self.plugins.setCategoriesFilter({
            "Runner" : IRunnerPlugin,
            "BDTest" : IBDTestPlugin,
            })
        self.plugins.setPluginPlaces(['%s/plugins' % os.path.dirname(os.path.realpath(__file__))])
        self.plugins.collectPlugins()
        for pluginInfo in self.plugins.getAllPlugins():
            self.plugins.activatePluginByName(pluginInfo.name)

    def initConnexion(self):
        try:
            #self.apiclient = TestlinkAPIClient(self.serverUrl, self.serverKey)
            print 'TODO'
        except:
            raise Exception("Connection impossible")
            pass

    def do_plugins(self, line):
        for categorie in self.plugins.getCategories():
            print colored('%s' % categorie, 'white')
            for pluginInfo in self.plugins.getPluginsOfCategory(categorie):
                print colored("%25s : %s" % (pluginInfo.name, pluginInfo.description), 'grey')
        print "runner actif : %s " % self.runner

    # LIST
    def do_list(self, content):
        #if content == 'projets':
        #    projets = self.apiclient.getProjects()
        #    for projet in projets:
        #        print "%6s --> %50s" % (projet['id'], projet['name'])
        #elif content == 'campagnes':
        #    if self.projetid == '0':
        #        #print colored('set projetid before', 'red')
        #        self.perror('set projetid before');
        #    else:
        #        campagnes = self.apiclient.getProjectTestPlans(testprojectid = self.projetid)
        #        for campagne in campagnes:
        #            print "%6s --> %50s" % (campagne['id'], campagne['name'])
        #elif content == 'tests':
        #    if self.campagneid == 0:
        #        print colored('set campagneid before', 'red')
        #    else:
        #        tests = self.apiclient.getTestCasesForTestPlan(testplanid=self.campagneid, execution_type=2)
        #        for (testid, test) in tests.items():
        #            print "%6s --> %50s" % (testid, test[0]['tcase_name'])
        #else:
        #    print "list"
        pass

    def complete_list(self, text, line, begidx, endidx):
        if not text:
            completions = self.LIST_OBJECTS[:]
        else:
            completions = [ f
                    for f in self.LIST_OBJECTS
                    if f.startswith(text)
                    ]
        return completions

    def help_list(self):
        print '\n'.join([ 'list [content]', 
                        ' list content from testlink'
                        ])

    # RUN
    def do_run(self, line):
        #starttime = datetime.datetime.now()
        #self.logger.info('Debut de la campagne : %s' % starttime)
        #i=0
        #tests = self.apiclient.getTestCasesForTestPlan(testplanid=self.campagneid, execution_type=2)
        #nbtest = len(tests)
        #resultLog=[]
        #progressbar = ProgressBar(maxval=nbtest, widgets=[Bar(marker='|')]).start()
        #for (testid, test) in tests.items():
        #    test_todo = test[0]
        #    notes=''
        #    script_behat = self.apiclient.getTestCaseCustomFieldDesignValue(testcaseexternalid=test_todo['full_external_id'],version=1,testprojectid=self.projetid,customfieldname='scriptBehat',details='full')
        #    scriptALancer=script_behat['value']
        #    browsers = self.apiclient.getTestCaseCustomFieldDesignValue(testcaseexternalid=test_todo['full_external_id'],version=1,testprojectid=self.projetid,customfieldname='Browsers',details='full')
        #    if browsers['value']=='':
        #        browserlist=['default']
        #    else:
        #        browserlist = browsers['value'].split('|')
        #    for browser in browserlist:
        #        notes = notes + " ====> Browser : %s\n" % browser
        #        runner = self.plugins.getPluginByName(self.runner)
        #        runner.plugin_object.run(browser,scriptALancer)
        #        (result, notes) = runner.plugin_object.result(browser,scriptALancer)
        #    try:
        #        retour = self.apiclient.reportTCResult(testcaseid=test_todo['tcase_id'],testplanid=self.campagneid,buildname='Validation bascule production',status=result,notes='Resultats du Test Auto (Behat) \n\n %s' % notes)
        #        if result=='p':
        #            msg='%6s : %60s : OK' % (testid, test_todo['tcase_name'])
        ##            resultLog.append(colored(msg,'green'))
        #            self.logger.info(msg)
        #        else:
        #            msg='%6s : %60s : NOK' % (testid, test_todo['tcase_name'])
        #            resultLog.append(colored(msg,'red'))
        #            self.logger.error(msg)
        #    except:
        #        try:
        #            retour = self.apiclient.reportTCResult(testcaseid=test_todo['tcase_id'],testplanid=self.campagneid,buildname='Validation bascule production',status=resultglobal,notes='Resultats du Test Auto (Behat) \n\n Erreur execution : site non accessible par exemple')
        #        except:
        #            retour = "Erreur de remonte de retour"
        #    i+=1
        #    progressbar.update(i)
        #progressbar.finish()
        #endtime = datetime.datetime.now()
        #self.logger.info('Fin de la campagne : %s' % endtime)
        #for i in resultLog:
        #    print i
        #difftime = endtime - starttime
        #print "Execution : %s" % difftime
        #self.logger.info('Temps Execution de la campagne : %s ' % difftime)
        pass

    def help_run(self):
        print '\n'.join(['run',
                         '  run campagne'
                         ])

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    logger = logging.getLogger('logger')
    logger.addHandler(logging.FileHandler(filename='testlinkconsole.log'))
    logger.setLevel(logging.INFO)
    console = TestLinkConsole(config, logger)
    console.initConnexion()
    console.cmdloop()
