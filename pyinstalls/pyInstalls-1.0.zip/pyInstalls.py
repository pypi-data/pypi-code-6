"""
https://docs.python.org/2/library/zipfile.html#zipfile-objects
https://docs.python.org/2/library/gzip.html
https://docs.python.org/2/library/os.path.html
C:\Users\usrname\AppData\Roaming\Microsoft\Windows\SendTo
self.fileName='C:\\Users\\rbeall\\Desktop\\arrow-0.4.4.tar.gz' #sys.arg[1]

C:\Users\usrname\AppData\Roaming\Microsoft\Windows\SendTo
%userprofile%\AppData\Roaming\Microsoft\Windows\SendTo
"""
import  os.path, shutil, tarfile, zipfile,  subprocess, sys 
class quickInstaller(): 

    def __init__(self, filePath):
        self.destination=os.path.expanduser("~\AppData\Local\Temp\unZipHere")  
        self.fileName=filePath
        
        #create folder if there isn't one
        self.makeUnzipFolder()                        
        
        #delete old files in destination
        self.deleteOld()  
        
        #unpacks zip, tar, gz
        self.getType(os.path.splitext(self.fileName)[1])
        
        #setup.py install
        self.installModule()              
        
    #make unzip folder if it doesn't exist        
    def makeUnzipFolder(self):       
        if not os.path.exists(self.destination): 
            os.makedirs(self.destination)   
    
    #delete old folder contents
    def deleteOld(self):     
        print 'trying to delete here %s ' % self.destination 
        folder=[root[0]+ dirs for root in os.walk(self.destination + '\\') for dirs in root[1]]
        if folder: 
            shutil.rmtree(folder[0])    

    #figure out what type of zip it is            
    def getType(self, fileExtension):
        typeDict={".zip":self.unZip, ".tar":self.unTar,".gz":self.gZip}
        typeDict[fileExtension]()            
                
    #install it                
    def installModule(self):        
        setupDirectory=[root[0] +'\\' for root in os.walk(self.destination)  for f in root[2] if f=='setup.py'][0]
        if setupDirectory:
            os.chdir(setupDirectory)   
            subprocess.call(["python", "setup.py", "install"])
        
    #im a zip, extract me
    def unZip(self):
        zipfile.ZipFile(self.fileName, 'r').extractall(self.destination)
    
    #im a gz, extract me            
    def gZip(self):
        tarfile.open(self.fileName,'r:gz').extractall(self.destination)
    
    #im a tar, extract me
    def unTar(self):
        tarfile.open(self.fileName,'r').extractall(self.destination)        

if __name__ == '__main__':
    installPlease=quickInstaller(sys.argv[1])
   
    








 
    