"""To build simple dialogues etc. (requires wxPython)
"""
# Part of the PsychoPy library
# Copyright (C) 2014 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).
from psychopy import logging
#from wxPython import wx
import wx
import numpy
import string, os

OK = wx.ID_OK

class Dlg(wx.Dialog):
    """A simple dialogue box. You can add text or input boxes
    (sequentially) and then retrieve the values.

    see also the function *dlgFromDict* for an **even simpler** version

    **Example:**    ::

        from psychopy import gui

        myDlg = gui.Dlg(title="JWP's experiment")
        myDlg.addText('Subject info')
        myDlg.addField('Name:')
        myDlg.addField('Age:', 21)
        myDlg.addText('Experiment Info')
        myDlg.addField('Grating Ori:',45)
        myDlg.addField('Group:', choices=["Test", "Control"])
        myDlg.show()  # show dialog and wait for OK or Cancel
        if myDlg.OK:  # then the user pressed OK
            thisInfo = myDlg.data
            print thisInfo
        else:
            print 'user cancelled'
    """
    def __init__(self,title='PsychoPy dialogue',
            pos=None, size=wx.DefaultSize,
            style=wx.DEFAULT_DIALOG_STYLE|wx.DIALOG_NO_PARENT,
            labelButtonOK = " OK ",
            labelButtonCancel = " Cancel "):
        style=style|wx.RESIZE_BORDER
        try:
            wx.Dialog.__init__(self, None,-1,title,pos,size,style)
        except:
            global app
            app = wx.PySimpleApp()
            wx.Dialog.__init__(self, None,-1,title,pos,size,style)
        self.inputFields = []
        self.inputFieldTypes= []
        self.inputFieldNames= []
        self.data = []
        #prepare a frame in which to hold objects
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.addText('')#insert some space at top of dialogue
        self.pos = pos
        self.labelButtonOK = labelButtonOK
        self.labelButtonCancel = labelButtonCancel
    def addText(self, text, color=''):
        textLength = wx.Size(8*len(text)+16, 25)
        myTxt = wx.StaticText(self,-1,
                                label=text,
                                style=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,
                                size=textLength)
        if len(color): myTxt.SetForegroundColour(color)
        self.sizer.Add(myTxt,1,wx.ALIGN_CENTER)

    def addField(self, label='', initial='', color='', choices=None, tip=''):
        """
        Adds a (labelled) input field to the dialogue box, optional text color
        and tooltip. Returns a handle to the field (but not to the label).
        If choices is a list or tuple, it will create a dropdown selector.
        """
        self.inputFieldNames.append(label)
        if choices:
            self.inputFieldTypes.append(str)
        else:
            self.inputFieldTypes.append(type(initial))
        if type(initial)==numpy.ndarray:
            initial=initial.tolist() #convert numpy arrays to lists
        container=wx.GridSizer(cols=2, hgap=10)
        #create label
        labelLength = wx.Size(9*len(label)+16,25)#was 8*until v0.91.4
        inputLabel = wx.StaticText(self,-1,label,
                                        size=labelLength,
                                        style=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        if len(color): inputLabel.SetForegroundColour(color)
        container.Add(inputLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        #create input control
        if type(initial)==bool:
            inputBox = wx.CheckBox(self, -1)
            inputBox.SetValue(initial)
        elif not choices:
            inputLength = wx.Size(max(50, 5*len(unicode(initial))+16), 25)
            inputBox = wx.TextCtrl(self,-1,unicode(initial),size=inputLength)
        else:
            inputBox = wx.Choice(self, -1, choices=[unicode(option) for option in list(choices)])
            # Somewhat dirty hack that allows us to treat the choice just like
            # an input box when retrieving the data
            inputBox.GetValue = inputBox.GetStringSelection
            initial = choices.index(initial) if initial in choices else 0
            inputBox.SetSelection(initial)
        if len(color): inputBox.SetForegroundColour(color)
        if len(tip): inputBox.SetToolTip(wx.ToolTip(tip))

        container.Add(inputBox,1, wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(container, 1, wx.ALIGN_CENTER)

        self.inputFields.append(inputBox)#store this to get data back on OK
        return inputBox

    def addFixedField(self,label='',value='',tip=''):
        """Adds a field to the dialogue box (like addField) but the field cannot
        be edited. e.g. Display experiment version. tool-tips are disabled (by wx).
        """
        thisField = self.addField(label,value,color='Gray',tip=tip)
        thisField.Disable() # wx disables tooltips too; we pass them in anyway
        return thisField

    def show(self):
        """Presents the dialog and waits for the user to press either OK or CANCEL.

        This function returns nothing.

        When they do, dlg.OK will be set to True or False (according to which
        button they pressed. If OK==True then dlg.data will be populated with a
        list of values coming from each of the input fields created.
        """
        #add buttons for OK and Cancel
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        OK = wx.Button(self, wx.ID_OK, self.labelButtonOK)
        OK.SetDefault()

        buttons.Add(OK)
        CANCEL = wx.Button(self, wx.ID_CANCEL, self.labelButtonCancel)
        buttons.Add(CANCEL)
        self.sizer.Add(buttons,1,flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM,border=5)

        self.SetSizerAndFit(self.sizer)
        if self.pos == None:
            self.Center()
        if self.ShowModal() == wx.ID_OK:
            self.data=[]
            #get data from input fields
            for n in range(len(self.inputFields)):
                thisName = self.inputFieldNames[n]
                thisVal = self.inputFields[n].GetValue()
                thisType= self.inputFieldTypes[n]
                #try to handle different types of input from strings
                logging.debug("%s: %s" %(self.inputFieldNames[n], unicode(thisVal)))
                if thisType in [tuple,list,float,int]:
                    #probably a tuple or list
                    exec("self.data.append("+thisVal+")")#evaluate it
                elif thisType==numpy.ndarray:
                    exec("self.data.append(numpy.array("+thisVal+"))")
                elif thisType in [str,unicode,bool]:
                    self.data.append(thisVal)
                else:
                    logging.warning('unknown type:'+self.inputFieldNames[n])
                    self.data.append(thisVal)
            self.OK=True
        else:
            self.OK=False
        self.Destroy()
        #    global app
        #self.myApp.Exit()



class DlgFromDict(Dlg):
    """Creates a dialogue box that represents a dictionary of values.
    Any values changed by the user are change (in-place) by this
    dialogue box.
    e.g.:

    ::

        info = {'Observer':'jwp', 'GratingOri':45, 'ExpVersion': 1.1, 'Group': ['Test', 'Control']}
        infoDlg = gui.DlgFromDict(dictionary=info, title='TestExperiment', fixed=['ExpVersion'])
        if infoDlg.OK:
            print info
        else: print 'User Cancelled'

    In the code above, the contents of *info* will be updated to the values
    returned by the dialogue box.

    If the user cancels (rather than pressing OK),
    then the dictionary remains unchanged. If you want to check whether
    the user hit OK, then check whether DlgFromDict.OK equals
    True or False

    See GUI.py for a usage demo, including order and tip (tooltip).
    """
    def __init__(self, dictionary, title='',fixed=[], order=[], tip={}):
        Dlg.__init__(self, title)
        self.dictionary=dictionary
        keys = self.dictionary.keys()
        keys.sort()
        if len(order):
            keys = order + list(set(keys).difference(set(order)))
        types=dict([])
        for field in keys:
            #DEBUG: print field, type(dictionary[field])
            types[field] = type(self.dictionary[field])
            tooltip = ''
            if field in tip.keys(): tooltip = tip[field]
            if field in fixed:
                self.addFixedField(field,self.dictionary[field], tip=tooltip)
            elif type(self.dictionary[field]) in [list, tuple]:
                self.addField(field,choices=self.dictionary[field], tip=tooltip)
            else:
                self.addField(field,self.dictionary[field], tip=tooltip)
        #show it and collect data
        #tmp= wx.PySimpleApp()#this should have been done by Dlg ?
        self.show()
        if self.OK:
            for n,thisKey in enumerate(keys):
                self.dictionary[thisKey]=self.data[n]

def fileSaveDlg(initFilePath="", initFileName="",
                prompt="Select file to save",
                allowed=None):
    """A simple dialogue allowing access to the file system.
    (Useful in case you collect an hour of data and then try to
    save to a non-existent directory!!)

    :parameters:
        initFilePath: string
            default file path on which to open the dialog
        initFilePath: string
            default file name, as suggested file
        prompt: string (default "Select file to open")
            can be set to custom prompts
        allowed: string
            a string to specify file filters.
            e.g. "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif"
            See http://www.wxpython.org/docs/api/wx.FileDialog-class.html for further details

    If initFilePath or initFileName are empty or invalid then
    current path and empty names are used to start search.

    If user cancels the None is returned.
    """
    if allowed==None:
        allowed = "All files (*.*)|*.*"  #\
            #"txt (*.txt)|*.txt" \
            #"pickled files (*.pickle, *.pkl)|*.pickle" \
            #"shelved files (*.shelf)|*.shelf"
    try:
        dlg = wx.FileDialog(None,prompt,
                          initFilePath, initFileName, allowed, wx.SAVE)
    except:
        tmpApp = wx.PySimpleApp()
        dlg = wx.FileDialog(None,prompt,
                          initFilePath, initFileName, allowed, wx.SAVE)
    if dlg.ShowModal() == OK:
        #get names of images and their directory
        outName = dlg.GetFilename()
        outPath = dlg.GetDirectory()
        dlg.Destroy()
        #tmpApp.Destroy() #this causes an error message for some reason
        fullPath = os.path.join(outPath, outName)
    else: fullPath = None
    return fullPath

def fileOpenDlg(tryFilePath="",
                tryFileName="",
                prompt="Select file to open",
                allowed=None):
    """A simple dialogue allowing access to the file system.
    (Useful in case you collect an hour of data and then try to
    save to a non-existent directory!!)

    :parameters:
        tryFilePath: string
            default file path on which to open the dialog
        tryFilePath: string
            default file name, as suggested file
        prompt: string (default "Select file to open")
            can be set to custom prompts
        allowed: string (available since v1.62.01)
            a string to specify file filters.
            e.g. "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif"
            See http://www.wxpython.org/docs/api/wx.FileDialog-class.html for further details

    If tryFilePath or tryFileName are empty or invalid then
    current path and empty names are used to start search.

    If user cancels, then None is returned.
    """
    if allowed==None:
        allowed = "PsychoPy Data (*.psydat)|*.psydat|"\
            "txt (*.txt,*.dlm,*.csv)|*.txt;*.dlm;*.csv|" \
            "pickled files (*.pickle, *.pkl)|*.pickle|" \
            "shelved files (*.shelf)|*.shelf|" \
            "All files (*.*)|*.*"
    try:
        dlg = wx.FileDialog(None, prompt,
                          tryFilePath, tryFileName, allowed, wx.OPEN|wx.FILE_MUST_EXIST|wx.MULTIPLE)
    except:
        tmpApp = wx.PySimpleApp()
        dlg = wx.FileDialog(None, prompt,
                          tryFilePath, tryFileName, allowed, wx.OPEN|wx.FILE_MUST_EXIST|wx.MULTIPLE)
    if dlg.ShowModal() == OK:
        #get names of images and their directory
        fullPaths = dlg.GetPaths()
    else: fullPaths = None
    dlg.Destroy()
    return fullPaths
