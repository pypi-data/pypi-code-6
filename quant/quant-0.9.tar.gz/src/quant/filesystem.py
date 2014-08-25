import os
import sys
import shutil
import dm.filesystem
from quant.dictionarywords import *

class FileSystem(dm.filesystem.FileSystem):

    isVerbose = '-v' in sys.argv or '--verbose' in sys.argv

    def make(self, path):
        if self.isVerbose:
            print "Creating folder: %s" % path
        os.makedirs(path)

    def remove(self, path, purpose):
        if self.isVerbose:
            print "Removing %s: %s" % (purpose, path)
        shutil.rmtree(path)

    def createProvisionDirs(self, provision):
        provisionPath = self.makeProvisionPath(provision)
        self.make(provisionPath)
        self.make(self.join(provisionPath, 'applications'))
        self.make(self.join(provisionPath, 'purposes'))
        self.make(self.join(provisionPath, 'migrationPlans'))

    def createPurposeDirs(self, purpose):
        purposePath = self.makePurposePath(purpose)
        self.make(purposePath)
        self.make(self.join(purposePath, 'etc'))

    def createApplicationDirs(self, application):
        applicationPath = self.makeApplicationPath(application)
        self.make(applicationPath)
        self.make(self.join(applicationPath, 'services'))
        self.make(self.join(applicationPath, 'dependencies'))

    def createServiceDirs(self, service):
        servicePath = self.makeServicePath(service)
        installPath = self.makeInstallPath(service)
        etcPath = self.makeEtcPath(service)
        varPath = self.makeVarPath(service)
        dataDumpsPath = self.makeDataDumpsPath(service)
        libPythonPath = self.makeLibPythonPath(service)
        self.make(servicePath)
        self.make(installPath)
        self.make(etcPath)
        self.make(varPath)
        self.make(dataDumpsPath)
        self.make(libPythonPath)

    def makeProvisionsPath(self):
        return self.dictionary[PROVISIONS_DIR_PATH]

    def makeProvisionPath(self, provision):
        provisionsPath = self.makeProvisionsPath()
        if not provision.name:
            raise Exception("Provision has no name: %s" % provision)
        return self.join(provisionsPath, provision.name)

    def makeMigrationPlanPath(self, migrationPlan):
        provisionPath = self.makeProvisionPath(migrationPlan.provision)
        return self.join(provisionPath, 'migrationPlans', migrationPlan.name)

    def makePurposePath(self, purpose):
        provisionPath = self.makeProvisionPath(purpose.provision)
        return self.join(provisionPath, 'purposes', purpose.name)

    def makePurposeApacheConfigPath(self, purpose):
        purposePath = self.makePurposePath(purpose)
        return self.join(purposePath, 'etc', 'httpd.conf')

    def makeServiceApacheConfigPath(self, service):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, 'etc', 'httpd.conf')

    def makeApplicationPath(self, application):
        provisionPath = self.makeProvisionPath(application.provision)
        return self.join(provisionPath, 'applications', application.name)

    def makeVePath(self, application):
        applicationPath = self.makeApplicationPath(application)
        return self.join(applicationPath, 've')

    def makeVeBinPath(self, application):
        vePath = self.makeVePath(application)
        return self.join(vePath, 'bin')

    def makeApplicationTarballPath(self, application, tarballBaseName=''):
        "Filesystem path to downloaded tarball."
        basePath = self.makeApplicationPath(application)
        fileName = self.makeApplicationTarballName(application)
        return self.join(basePath, fileName)

    def makeApplicationTarballName(self, application):
        if application.location and 'using ' not in application.location:
            return self.basename(application.location)
        else:
            return self.makeTarballName(
                #self.tarballBaseName or application.provision.name, application.name
                application.provision.name, application.name
            )

    def makeTarballName(self, name, version):
        return "%s-%s.tar.gz" % (name, version)

    def makeDependenciesPath(self, dependency):
        applicationPath = self.makeApplicationPath(dependency.application)
        return self.join(applicationPath, 'dependencies')

    def makeDependencyPath(self, dependency):
        dependenciesPath = self.makeDependenciesPath(dependency)
        fileName = self.basename(dependency.location) or "%s.tar.gz" % dependency.name 
        return self.join(dependenciesPath, fileName)

    def makeServicePath(self, service):
        applicationPath = self.makeApplicationPath(service.application)
        return self.join(applicationPath, 'services', service.name)

    def makeDataDumpsPath(self, service):
        servicePath = self.makeServicePath(service)
        return self.join(servicePath, 'dataDumps')

    def makeDataDumpPath(self, dataDump):
        dumpsPath = self.makeDataDumpsPath(dataDump.service)
        return self.join(dumpsPath, dataDump.name)

    def makeDomainModelDumpPath(self, dataDump):
        dumpPath = self.makeDataDumpPath(dataDump)
        return self.join(dumpPath, 'domainModelDump')

    def makeFilesDumpDirPath(self, dataDump):
        dumpPath = self.makeDataDumpPath(dataDump)
        return self.join(dumpPath, 'filesDump')

    def makeInstallPath(self, service):
        servicePath = self.makeServicePath(service)
        return self.join(servicePath, 'live')

    def makeLogFilePath(self, service):
        varPath = self.makeVarPath(service)
        systemName = self.dictionary[SYSTEM_NAME]
        return self.join(varPath, 'log', '%s.log' % systemName)

    def makeBinPath(self, service):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, 'bin')

    def makeEtcPath(self, service):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, 'etc')

    def makeVarPath(self, service):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, 'var')

    def makeAdminScriptPath(self, service):
        binPath = self.makeBinPath(service)
        fileName = '%s-admin' % self.domainObject.name
        return self.join(binPath, fileName)

    def makeTestScriptPath(self, service):
        binPath = self.makeBinPath(service)
        fileName = '%s-test' % self.domainObject.name
        return self.join(binPath, fileName)

    def makeLibPythonPath(self, service):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, 'lib', 'python')

    def makeScriptRunnerPath(self, service):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, 'scriptrunner')

    def makeConfigPath(self, service):
        etcPath = self.makeEtcPath(service)
        filename = self.configFilename(service.application.provision.name)
        return self.join(etcPath, filename)

    def provisionDirExists(self, provision):
        provisionPath = self.makeProvisionPath(provision)
        return self.exists(provisionPath)

    def configFilename(self, name):
        return '%s.conf' % name
    
    def makeTemplatesPath(self, service):
        return self.join(self.makeInstallPath(service), 'templates')

    def makeExampleConfigPath(self, service, name):
        installPath = self.makeInstallPath(service)
        return self.join(installPath, self.relExampleConfigPath(service.application.provision.name))

    def relExampleConfigPath(self, name):
        return self.join('etc', '%s.conf.new' % name)

    def validateDirPath(self, path):
        if not self.exists(path):
            raise Exception("Path not found: %s" % path)
        if not self.isdir(path):
            raise Exception("Path not a dir: %s" % path)

    def validateSourcePath(self, path):
        if not path:
            raise Exception("No source path quantd.")

    def chdirProvisions(self):
        dirPath = self.dictionary[PROVISIONS_DIR_PATH]
        self.chdir(dirPath)

    def chdir(self, dirPath):
        try:
            os.chdir(dirPath)
        except OSError, inst:
            raise Exception("Couln't change directory to: %s" % inst)

    def join(self, *args, **kwds):
        return os.path.join(*args, **kwds)

    def isdir(self, *args, **kwds):
        return os.path.isdir(*args, **kwds)

    def exists(self, *args, **kwds):
        return os.path.exists(*args, **kwds)
