
#
# NuGridpy - Tools for accessing and visualising NuGrid data.
#
# Copyright 2007 - 2014 by the NuGrid Team.
# All rights reserved. See LICENSE.
#

""" 
ppm.py

By Daniel Alexander Bertolino Conti

Fall 2010

PPM is a Python module for reading Yprofile-01-xxxx.bobaaa files.
Simple session for working with ppm.py, here I assume user's working
directory contains some YProfile files.

If the user find any bugs or errors, please email.

Yprofile files Assumptions
==========================

- labeled as YProfile-01-xxxx.bobaaa and the xxxx is the NDump that is
  located within each file.

- There can be a maximum of 9999 files in each directory.  The first 10
  lines of each file are the only place where header data is uniquely
  located.

- Header data is separated by five spaces and line breaks.

- An attribute cant be in the form of a number, ie if the user is able
  to 'float(attribute)' (in python) without an error attribute will not
  be returned.

- A row of column Names or Cycle Names is preceded and followed by a
  blank line.

- A block of data values are preceded and followed by a blank line
  except the last data block in the file, where it is not followed by a
  blank line.

- In the YProfile file, if a line of attributes contains the attribute
  Ndump, then that line of attributes and any other following lines of
  attributes in the file are cycle attributes.

Header Attribute Assumptions
============================

- Header attributes are separated by lines and instances of four spaces
  (    )

- Header attribute come in one of below here are things that do stuff
  with the data 6 types.

- The first type is the first attribute in the file. It is formatted in
  such a way that the name of the attribute is separated from its
  associated data with an equals sign ex.
  Stellar Conv. Luminosity =  1.61400E-02 x 10^43 ergs,

- The second type is when an attribute contains the sub string 'grid;'.
  It is formatted in such a way such that there are 3 numerical values
  separated by 'x' which are then followed by the string ' grid;' ex.
  384 x 384 x 384 grid;

- The third type is were name of the attribute is separated from its
  associated data with an equals sign.  Also that data may be followed
  by a unit of measurement. ex.
  Thickness (Mm) of heating shell =  1.00000E+00

- The fourth type is when an attribute contains a colon.  The String
  before the colon is the title of the attribute.  After the colon there
  is a list of n sub attributes, each with a sub title, and separated by
  its value with an equals sign.  Aslo each sub attribute is separated
  by a comma ex.
  At base of the convection zone:  R =  9.50000E+00,  g =  4.95450E-01,
  rho =  1.17400E+01,  p =  1.69600E+01

- The fifth is when an attribute starts with 'and'.  after the and, the
  next word after has to be the same as one word contained in the
  previous attribute ex.
  and of transition from convection to stability =  5.00000E-01  at
  R =  3.00000E+01 Mm.

- The sixth is when there is a string or attribute title followed by two
  spaces followed by one value followed by two spaces followed by an
  'and' which is then followed by a second Value ex.
  Gravity turns on between radii   6.00000E+00  and   7.00000E+00  Mm.

Examples
========
Here is an example runthrough.

>>> from ppm import *
>>> p=y_profile()
>>> head= p.hattri
>>> cols= p.dcols
>>> cyc=p.cattri
>>> print head
[['Stellar Conv. Luminosity', '1.61400E-02 x 10^43 ergs,'], ['384 x 384 x 384 grid;'], ... ]
>>> print cols
['j', 'Y', 'FVconv', 'UYconv', ... , 'Ek H+He']
>>> print cyc
['Ndump', 't', 'trescaled', 'Conv Ht', 'H+He Ht', ..., 'EkXZHHeMax']
>>> j2=p.getColData('j','Yprofile-01-0002',numType='file',resolution='a')
>>> print j2
[[384.0, 383.0, 382.0,..., 1.0],[192.0, 191.0, 190.0,...,1.0]]
>>> j2=p.get('j')
>>> print j2
[[384.0, 383.0, 382.0,..., 1.0],[192.0, 191.0, 190.0,...,1.0]]
>>> j55=p.getColData('j',55,numType='t',resolution='l')
The closest time is at Ndump = 2
>>> print j55
>>> y=p.getColData('Rho1 H+He',2, resolution='L')
>>> print y
[2.0420099999999999e-07, 5.4816300000000004e-07, ... , 0]

and

>>> p.plot('j','FVconv')

plots the data.

"""
from numpy import *
from math import *
from data_plot import *
import matplotlib.pylab as pyl
import matplotlib.pyplot as pl
import os

class yprofile(DataPlot):
    """ 
    Data structure for holding data in the  YProfile.bobaaa files.
    
    Parameters
    ----------
    sldir : string
        which directory we are working in.  The default is '.'.
        
    """

    def __init__(self, sldir='.'):
        """ 
        init method

        Parameters
        ----------
        sldir : string
            which directory we are working in.  The default is '.'.
        
        """

        self.files = []  # List of files in this directory
        self.cycles= []  # list of cycles in this directory
        self.hattrs = [] # header attributes
        self.dcols = []  # list of the column attributes
        self.cattrs= []  # List of the attributes of the y profiles
        self._cycle=[]    # private var
        self._top=[]      # privite var
        self.sldir = sldir #Standard Directory

        if not os.path.exists(sldir):  # If the path does not exist
            print 'error: Directory, '+sldir+ ' not found'
            print 'Now returning None'
            return None
        else:
            f=os.listdir(sldir) # reads the directory
            for i in range(len(f)):  # Removes any files that are not YProfile files
                if 'YProfile' in f[i] and '.bobaaa' in f[i] and 'ps' not in f[i] :
                    self.files.append(f[i])

            self.files.sort()
            if len(self.files)==0: # If there are no YProfile Files in thes Directory
                print 'Error: no YProfile named files exist in Directory'
                print 'Now returning None'
                return None
            slname=self.files[len(self.files)-1] #
            print "Reading attributes from file ",slname
            self.hattrs,self.dcols, self._cycle=self._readFile(slname,sldir)

            self._splitHeader() #Splits the HeaTder into header attributes and top attributes
            self.hattrs=self._formatHeader() # returns the header attributes as a dictionary
            self.cattrs=self.getCattrs() # returns the concatination of Cycle and Top Attributes

            self.ndumpDict=self.ndumpDict(self.files)

            print 'There are '+str(len(self.files))+' YProfile files in the ' +self.sldir+' directory.'
            print 'Ndump values range from '+str(min(self.ndumpDict.keys()))+' to '+str(max(self.ndumpDict.keys()))
            t=self.get('t',max(self.ndumpDict.keys()))
            t1=self.get('t',min(self.ndumpDict.keys()))
            print 'Time values range from '+ str(t1[-1])+' to '+str(t[-1])
            self.cycles=self.ndumpDict.keys()
        return None

    def ndumpDict(self, fileList):
        """ 
        Method that creates a dictionary of Filenames with the
        associated key of the filename's Ndump.
        
        Parameters
        ----------
        fileList : list
            A list of yprofile filenames.
            
        Returns
        -------
        dictionary
            the filenamem, ndump dictionary
            
        """
        ndumpDict={}
        for i in xrange(len(fileList)):
            ndump=fileList[i].split("-")[-1]
            ndump=ndump.split(".")[0]
            ndumpDict[int(ndump)]=fileList[i]

        return ndumpDict

    def getHattrs(self):
        """ returns the list of header attributes"""
        h=self.hattrs.sorted()
        return h.sort()

    def getDCols(self):
        """ returns the list of column attributes"""
        return self.dcols

    def getCattrs(self):
        """ returns the list of cycle attributes"""
        dupe=False
        data=[]
        for i in range(len(self._cycle)):
            data.append(self._cycle[i])

        for i in range(len(self._top)): # checking for dublicate attributes
                                        # ie if an Atribute is both a top attri and a cycle attri
            for k in range(len(self._cycle)):
                if self._top[i]==self._cycle[k]:
                    dupe=True
            if not dupe:
                data.append(self._top[i])
            dupe=False

        return data

    def get(self, attri, fname=None, numtype='ndump', resolution='H'):
        """ 
        Method that dynamically determines the type of attribute that is
        passed into this method.  Also it then returns that attribute's
        associated data.

        Parameters
        ----------
        attri : string
            The attribute we are looking for.
        fname : string, optional
            The filename, Ndump or time, if None it defaults to the
            last NDump.  The default is None.
        numtype : string, optional
            Designates how this function acts and how it interprets
            fname.  If numType is 'file', this function will get the
            desired attribute from that file.  If numType is 'NDump'
            function will look at the cycle with that nDump.  If
            numType is 'T' or 'time' function will find the _cycle
            with the closest time stamp.  The default is "ndump".
        Resolution : string, optional
            Data you want from a file, for example if the file contains
            two different sized columns of data for one attribute, the
            argument 'a' will return them all, 'h' will return the
            largest, 'l' will return the lowest. The default is 'H'.

        """
        isCyc=False #If Attri is in the Cycle Atribute section
        isCol=False #If Attri is in the Column Atribute section
        isHead=False #If Attri is in the Header Atribute section

        if fname==None:
            fname=max(self.ndumpDict.keys())

        if attri in self.cattrs: # if it is a cycle attribute
            isCyc = True
        elif attri in self.dcols:#  if it is a column attribute
            isCol = True
        elif attri in self.hattrs:# if it is a header attribute
            isHead = True

        # directing to proper get method
        if isCyc:
            return self.getCycleData(attri,fname, numtype, resolution=resolution)
        if isCol:
            return self.getColData(attri,fname, numtype, resolution=resolution)
        if isHead:
            return self.getHeaderData(attri)
        else:
            print 'That Data name does not appear in this YProfile Directory'
            print 'Returning none'
            return None

    def getHeaderData(self, attri):
        """ 
        Parameters
        ----------        
        attri : string
            The name of the attribute.
        
        Returns
        -------
        string or integer
            Header data that is associated with the attri.

        Notes
        -----
        To see all possable options in this instance type
        instance.getHattrs().
        
        """
        isHead = False
        if attri in self.hattrs:
            isHead = True
        if not isHead:# Error checking
            print 'The attribute '+attri+' does not appear in these YProfiles'
            print 'Returning None'
            return None
        data=self.hattrs[attri] #Simple dictionary access
        return data

    def getCycleData(self, attri, FName=None, numType='ndump',
                     Single=False, resolution='H'):
        """ 
        Parameters
        ----------
        attri : string
            What we are looking for.
        FName : string, optional
            The filename, Ndump or time, if None it defaults to the last
            NDump.  The default is None.
        numType : string, optional
            Designates how this function acts and how it interprets
            FName.  If numType is 'file', this function will get the
            desired attribute from that file.  If numType is 'NDump'
            function will look at the cycle with that nDump.  If
            numType is 'T' or 'time' function will find the _cycle
            with the closest time stamp.  The default is "ndump".
        Single : boolean, optional
            Determining whether the user wants just the Attri contained
            in the specified ndump or all the dumps below that ndump.
            The default is False.
        Resolution : string, optional
            Data you want from a file, for example if the file contains
            two different sized columns of data for one attribute, the
            argument 'a' will return them all, 'h' will return the
            largest, 'l' will return the lowest.  The defalut is 'H'.

        Returns
        -------
        list
            A Datalist of values for the given attribute or a
            single attribute in the file FName.

        """
        isCyc= False #If Attri is in the Cycle Atribute section
        boo=True
        filename=self.findFile(FName, numType)
        data=0

        if FName==None: #By default choose the last YProfile
            FName=max(self.ndumpDict.keys())

        if attri in self._cycle: #if attri is a cycle attribute rather than a top attribute
            isCyc = True

        if attri not in self._cycle and isCyc:# Error checking
            print 'Sorry that Attribute does not appear in the fille'
            print 'Returning None'
            return None

        if not Single and isCyc:

            data= self.getColData( attri,filename,'file',resolution, True)

            return data
        if Single and isCyc:

            data= self.getColData( attri,filename,'file',resolution, True)
            if data==None:
                return None
            index=len(data)-1
            return data[index]
        if not Single and not isCyc:

            data=[]
            i=0
            while boo: #Here we basically open up each YProfile File and append the required top attribute
                       # to our data variable
                data.append(self.readTop(attri,self.files[i],self.sldir))
                if self.files[i]==filename: #if we have reached the final file that the user wants.
                    boo=False
                i+=1
            for j in range(len(data)): #One top attribute hase a value of '*****' we cant float that, so we ignore it here
                if '*' not in data[j]:
                    data[j]=float(data[j])

            data=array(data)
        if Single and not isCyc:

            data=self.readTop(attri,filename,self.sldir)
            data=float(data)

        return data

    def getColData(self, attri, FName, numType='ndump', resolution='H',
                   cycle=False):
        """ 
        Parameters
        ----------
        attri : string
            Attri is the attribute we are loking for.
        FName : string
            The name of the file, Ndump or time we are looking for.
        numType : string, optional
            Designates how this function acts and how it interprets
            FName.  If numType is 'file', this function will get the
            desired attribute from that file.  If numType is 'NDump'
            function will look at the cycle with that nDump.  If
            numType is 'T' or 'time' function will find the _cycle
            with the closest time stamp.  The default is "ndump".
        Resolution : string, optional
            Data you want from a file, for example if the file contains
            two different sized columns of data for one attribute, the
            argument 'a' will return them all, 'h' will return the
            largest, 'l' will return the lowest.  The defalut is 'H'.
        cycle : boolean, optional
            Are we looking for a cycle or column attribute.
            The default is False.

        Returns
        -------
        list
            A Datalist of values for the given attribute.

        Notes
        -----
        To ADD: options for a middle length of data.

        """
        num=[]       #temp list that holds the line numbers where the
                     # attribute is found in
        dataList=[]  # holds final data
        attriLine='' # hold a line that the attribute is found in
        attriList=[] # holds a list of attributes that the attribute is
                     # found in
        numList=[]   # holds a single column of data
        boo=False     #temp boolean
        tmp=''

        FName=self.findFile(FName, numType)
        #print FName
        stddir=self.sldir
        resolution=resolution.capitalize()
        if stddir.endswith('/'):  # Makeing sure that the standard dir ends with a slash
                                  # So we get something like /dir/file instead of /dirfile
            FName = str(stddir)+str(FName)
        else:
            FName = str(stddir)+'/'+str(FName)


        boo=True
        try:
            f=open(FName, 'r')
        except IOError:
            print "That File, "+FName+ ", does not exist."
            print 'Returning None'
            return None
        List=f.readlines()
        f.close()
        for i in range(len(List)):#finds in what lines the attribute is
                                  #located in. This is stored in num, a list of line numbers
            tmpList=List[i].split('  ')
            for k in range(len(tmpList)):
                tmpList[k]=tmpList[k].strip()

            for k in range(len(tmpList)):
                if not cycle:
                    if attri == tmpList[k] and not('Ndump' in List[i]): #if we are looking for a column attribute
                        num.append(i)
                else:
                    if attri == tmpList[k] and ('Ndump' in List[i]): #if we are looking for a cycle attribute
                        num.append(i)

        #print num

        if i==(len(List) -1) and len(num)==0: #error checking
            print "Attribute DNE in file, Returning None"
            return None

        for j in range(len(num)): #for each line that attri appears in
            attriList=[]
            rowNum=num[j] #the line in the file that the attribute
                          #appears at
            attriLine=List[rowNum]

            tmpList=attriLine.split('  ') #tmplist will be a list of
                                          #attributes
            for i in range(len(tmpList)):#formating tmplist
                tmpList[i]=tmpList[i].strip()
                if tmpList[i]!='':
                    attriList.append(tmpList[i])

            for i in range(len(attriList)):
                # here we find at what element in the list attri
                # appears at, this value bacomes colNum
                if attri == attriList[i]:
                    break
            colNum=i

            rowNum+=2 #Since the line of Data is two lines after
                      #the line of attributes


            while rowNum<len(List)and List[rowNum]!= '\n': #and rowNum<len(List)-1:
                # while we are looking at a line with data in it
                # and not a blank line and not the last line in
                # the file
                tmpList=List[rowNum].split(None) #split the line
                                         #into a list of data
                #print tmpList
                numList.append(tmpList[colNum])
                #append it to the list of data
                rowNum+=1

            #Because an attributes column of data may appear more
            #than onece in a file, must make sure not to add it twice
            if len(dataList)==0: #No data in dataList yet, no need to check
                dataList.append(numList)

            else:
                for k in range(len(dataList)):
                    #if a list of data is allready in the
                    #dataList with the same length of numList
                    #it means the data is allready present, do not add
                    if len(numList)== len(dataList[k]):
                        boo=False

                if boo:
                    dataList.append(numList)


                boo = True

            numList=[]

        tmp=''


        tmpList=[]



        #here we format the data if the user wants higher or the lower resolution of data
        if resolution.startswith('H'):
            for i in range(len(dataList)):
                if len(dataList[i])>len(tmp):
                    tmp=dataList[i]
            dataList=array(tmp,dtype=float)
        elif resolution.startswith('L'):
            for i in range(len(dataList)):
                if len(dataList[i])<len(tmp) or len(tmp)==0:
                    tmp=dataList[i]
            dataList=array(tmp,dtype=float)
        else:
            for i in range(len(dataList)):
                for k in range(len(dataList[i])):
                    dataList[i][k]=float(dataList[i][k])
                    dataList[i][k]=float(dataList[i][k])
                dataList[i]=array(dataList[i])

            try: # If dataList is a list of lists that has one element [[1,2,3]]
            # reformat dataList as [1,2,3]
                j=dataList[1][0]
            except IndexError:
                tmp = True
            except TypeError:
                tmp = False
            if tmp:
                dataList=dataList[0]



        tmp = False



        return dataList

    def findFile(self, FName, numType='FILE'):
        """ 
        Function that finds the associated file for FName when Fname
        is time or NDump.
        
        Parameters
        ----------
        FName : string
            The name of the file, Ndump or time we are looking for.
        numType : string, optional
            Designates how this function acts and how it interprets
            FName.  If numType is 'file', this function will get the
            desird attribute from that file.  If numType is 'NDump'
            function will look at the cycle with that nDump.  If
            numType is 'T' or 'time' function will find the cycle with
            the closest time stamp.  The default is "FILE".
            
        """

        numType=numType.upper()
        boo=False
        indexH=0
        indexL=0
        if numType=='FILE':

            #do nothing
            return str(FName)

        elif numType=='NDUMP':
            try:    #ensuring FName can be a proper NDump, ie no letters
                FName=int(FName)
            except:
                print 'Improper value for NDump, choosing 0 instead'
                FName=0
            if FName < 0:
                print 'User Cant select a negative NDump'
                print 'Reselecting NDump as 0'
                FName=0
            if FName not in self.ndumpDict.keys():
                print 'NDump '+str(FName)+ ' Does not exist in this directory'
                print 'Reselecting NDump as the largest in the Directory'
                print 'Which is '+ str(max(self.ndumpDict.keys()))
                FName=max(self.ndumpDict.keys())
            boo=True

        elif numType=='T' or numType=='TIME':
            try:    #ensuring FName can be a proper time, ie no letters
                FName=float(FName)
            except:
                print 'Improper value for time, choosing 0 instead'
                FName=0
            if FName < 0:
                print 'A negative time does not exist, choosing a time = 0 instead'
                FName=0
            timeData=self.get('t',self.ndumpDict[max(self.ndumpDict.keys())],numtype='file')
            keys=self.ndumpDict.keys()
            keys.sort()
            tmp=[]
            for i in xrange(len(keys)):
                tmp.append(timeData[keys[i]])

            timeData=tmp
            time= float(FName)
            for i in range(len(timeData)): #for all the values of time in the list, find the Ndump that has the closest time to FName
                if timeData[i]>time and i ==0:
                    indexH=i
                    indexL=i
                    break
                if timeData[i]>time:
                    indexH=i
                    indexL=i-1
                    break
                if i == len(timeData)-1:
                    indexH=i
                    indexL=i-1
            high=float(timeData[indexH])
            low= float(timeData[indexL])
            high=high-time
            low=time-low

            if high >=low:
                print 'The closest time is at Ndump = ' +str(keys[indexL])
                FName=keys[indexL]
            else:
                print 'The closest time is at Ndump = ' +str(keys[indexH])
                FName=keys[indexH]
            boo=True
        else:
            print 'Please enter a valid numType Identifyer'
            print 'Returning None'
            return None

        if boo:#here i assume all yprofile files start like 'YProfile-01-'
            FName=self.ndumpDict[FName]
        return FName

    def _splitHeader(self):
        """ 
        Private function that splits up the data in the header section of the YProfile
        into header attributes and top attributes, where top attributes are just
        cycle attributes located in the header section of the YProfile

        """
        tmp=[]
        tmp2=[]
        slname=self.files[0]
        header, tm, tm1=self._readFile(slname,self.sldir) # Find the header section from another YProfile


        if len(header)!=len(self.hattrs): #error checking
            print 'Header atribute error, directory has two YProfiles that have different header sections'
            print 'Returning unchanged header'
            return None
        for i in range(len(header)):
            if header[i]==self.hattrs[i]: #if the headers are bothe the same, that means its a
                tmp.append(header[i]) #header attribute
            else:                         #Else it changes cycle to cycle and therfore
                                          #its a cycle attribute
                tmp2.append(header[i])

        for i in range(len(tmp2)):            #Formats the top attributes
            tmp2[i]=tmp2[i][0]            #Ie splits the attributes from its associated data.


        self.hattrs=tmp
        self._top=tmp2

    def _formatHeader(self):
        """ 
        Private function that takes in a set of header attributes and
        then Formats them into a dictionary.

        Input -> A List of headers in the proper format

        Assumptions
        ===========
        
        The first element in the list is Stellar Conv. Luminosity header

        The output in the dictionary looks like
        {'Stellar Conv. Luminosity':The associated data}.

        If an element contains the string 'grid;' it is the grid size
        header and the first, second and third are the x, y and z grid
        sizes respectively.

        The output in the dictionary looks like
        {'gridX':9,'gridY':9,'gridZ':9}.
        
        If an element is size two the first item is the header name and
        the second will be its associated value.

        The output in the dictionary looks like {'First Item':value}
        
        If an element contains a colon, The string preceding the colon
        is one part of the header name.  The string after the colon
        will be a list of associations in the form of the name followed
        by an equals sign followed by its value.
        
        for example a line like this would look like:

        """
        headers=self.hattrs
        dic={}
        i=0
        print "Analyzing headers ..."
        while i < len(headers):
            if i ==0: # If it is the Stellar Luminosity attribute
                tmp=headers[i][1]
                """
                if '^' in tmp[2]:


                        j=tmp[2].split('^')
                        j=float(j[0])**float(j[1])
                else:
                        j=tmp[2]
                tmp=float(tmp[0])*float(j)
                """

                dic[headers[i][0]]=tmp
                i+=1

            elif 'grid;' in headers[i][0]: # If its the grid header attribute
                tmp1=[]
                tmp= headers[i][0].split()

                for j in range(len(tmp)):
                    tmp[j]=tmp[j].strip('x')
                    tmp[j]=tmp[j].strip('')
                for j in range(len(tmp)):
                    if tmp[j]!='':
                        tmp1.append(tmp[j])
                tmp=tmp1
                dic['gridX']=tmp[0]
                dic['gridY']=tmp[1]
                dic['gridZ']=tmp[2]
                i+=1

            elif len(headers[i])==2: # If its the header attribute that is seperated by a single = sign
                tmp=headers[i][1]

                dic[headers[i][0]]=tmp
                i+=1

            elif ':' in headers[i][0]: #If its the header attribute like 'Title: a=2, b=3
                tmp=headers[i][0].split(':')
                tmp2=tmp[1].split(',')
                for j in range(len(tmp2)):
                    tmp3=tmp2[j].split('=')
                    for k in range(len(tmp3)):
                        tmp3[k]=tmp3[k].strip()
                    dic[tmp[0]+' '+tmp3[0]]=tmp3[1]
                i+=1

            elif headers[i][0].startswith('and '):

                tmp=headers[i][0].split('=',1)

                tmp2=tmp[0].lstrip('and')
                tmp2=tmp2.lstrip()
                prev=headers[i-1][0].split()
                curr=tmp2.split()
                curr=curr[0]
                tmp3=''
                for j in range(len(prev)):
                    if prev[j]== curr:
                        break;
                    tmp3+=prev[j]+' '
                tmp2=tmp3+tmp2
                dic[tmp2]=tmp[1].strip()
                i+=1

            else:
                tmp=headers[i][0].split('  ')
                for j in range(len(tmp)):
                    tmp[j]=tmp[j].strip()
                dic[tmp[0]+' Low']=tmp[1]
                dic[tmp[0]+' High']=tmp[3]
                i+=1
        return dic

# below are some utilities that the user typically never calls directly
    def readTop(self,atri,filename,stddir='./'):
        """ 
        Private routine that Finds and returns the associated value for
        attribute in the header section of the file.
        
        Input:
        atri, what we are looking for.
        filename where we are looking.
        StdDir the directory where we are looking, Defaults to the
        working Directory.

        """
        if stddir.endswith('/'):
            filename = str(stddir)+str(filename)
        else:
            filename = str(stddir)+'/'+str(filename)
        f=open(filename,'r')
        headerLines=[]
        header=[]
        headerAttri=[]
        for i in range(0,10): # Read out the header section of the file.
            line = f.readline()
            line=line.strip()
            if line != '':
                headerLines.append(line)
        f.close()
        for i in range(len(headerLines)): #for each line of header data split up the occurances of '    '
            header.extend(headerLines[i].split('     '))
            header[i]=header[i].strip()

        for i in range(len(header)):
            tmp=header[i].split('=')# for each line split up on occurances of =
            if len(tmp)!=2: # If there are not two parts, add the unsplit line to headerAttri
                tmp=[]
                tmp.append(header[i].strip())
                headerAttri.append(tmp)
            elif len(tmp)==2: # If there are two parts, add the list of the two parts to headerAttri
                tmp[0]=tmp[0].strip()
                tmp[1]=tmp[1].strip()
                headerAttri.append([tmp[0],tmp[1]])

        for i in range(len(headerAttri)):
            if atri in headerAttri[i]: # if the header arrtibute equals atri, return its associated value
                value=headerAttri[i][1]

        value =value.partition(' ')
        value=value[0]
        return value

    def _readFile(self,filename,stddir='./'):
        """ 
        private routine that is not directly called by the user.
        filename is the name of the file we are reading
        stdDir is the location of filename, defaults to the
        working directory
        Returns a list of the header attributes with their values
        and a List of the column values that are located in this
        particular file and a list of directory attributes.
        
        Assumprions:
        *An attribute cant be in the form of a num, if
        the user can float(attribute) without an error
        attribute will not be returned
        Lines of attributs are followd and preceded by
        *blank lines

        """
        if stddir.endswith('/'):
            filename = str(stddir)+str(filename)
        else:
            filename = str(stddir)+'/'+str(filename)

        f=open(filename,'r')
        line=''
        headerLines=[] # List of lines in the header section of the YProfile
        header=[]      # Single line of header data
        tmp=[]
        tmp2=[]
        headerAttri=[] # Final list of header Data to be retruned
        colAttri=[]    # Final list of column attributes to be returned
        cycAttri=[]    # Final list of cycle attributes to be returned
        for i in range(0,10): # read the first 10 lines of the YProfile
                              # Add the line to headerLines if the line is not empty
            line = f.readline()
            line=line.strip()
            if line != '':
                headerLines.append(line)

        for i in range(len(headerLines)): # For each line split on occurances of '    '
                                          # And then clean up any extra whitespace.
            header.extend(headerLines[i].split('     '))
            header[i]=header[i].strip()

        for i in range(len(header)):# for each line split up on occurances of =
            tmp=header[i].split('=')
            if len(tmp)!=2: # If there are not two parts, add the unsplit line to headerAttri
                tmp=[]
                tmp.append(header[i].strip())
                headerAttri.append(tmp)
            elif len(tmp)==2: # If there are two parts, add the list of the two parts to headerAttri
                tmp[0]=tmp[0].strip()
                tmp[1]=tmp[1].strip()
                headerAttri.append([tmp[0],tmp[1]])

        lines= f.readlines()
        boo = True
        ndump=False
        attri=[]
        for i in range(len(lines)-2): #for the length of the file
            if lines[i] =='\n'and lines[i+2]=='\n': # If there is a blank line,
                #that is followed by some line and by another blank line
                # it means the second line is a line of attributes
                line = lines[i+1] # line of attributes

                line=line.split('  ') # split it up on occurances of '  '

                for j in range(len(line)): #Clean up any excess whitespace
                    if line[j]!='':    #And add it to a list of attributes
                        attri.append(line[j].strip())

                for j in range(len(attri)):
                    """
                    if attri[j]=='Ndump':
                            i = len(lines)
                            break
                            """
                    for k in range(len(colAttri)):  #If it is not allready in the list of Attributes
                                                    # add it
                        if colAttri[k]==attri[j]:
                            boo = False
                            break
                    if boo :
                        colAttri.append(attri[j])
                    boo=True

        tmp=[]
        for i in range(len(colAttri)):#gets rid of blank lines in the list
            if colAttri[i]!='':
                tmp.append(colAttri[i])
        colAttri=tmp
        tmp=[]
        for i in range(len(colAttri)):#gets rid of numbers in the list
            try:
                float(colAttri[i])
            except ValueError:
                tmp.append(colAttri[i])
        colAttri=tmp
        tmp=[]
        # NOTE at this point in the program colAttri is a unified list of Column attributes and Cycle Attributes


        for i in range(len(colAttri)): #Here we split up our list into Column attributes and Cycle Attributes
            if colAttri[i]=='Ndump':
                # If we get to Ndump in our list of attributes, then any following attributes are cycle attributes
                ndump=True
            if not ndump:
                tmp.append(colAttri[i])
            else:
                cycAttri.append(colAttri[i])

        colAttri=tmp
        f.close()
        return headerAttri,colAttri, cycAttri
