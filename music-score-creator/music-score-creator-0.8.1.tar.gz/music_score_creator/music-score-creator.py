#!/usr/bin/env python

    # <Music score creator. Generate a sheet music from an audio.>
    # Copyright (C) <2014>  <Jose Carlos Montanez Aragon>

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import os
import wx
import time
import music_score_creator
from music_score_creator.sound import *
#from sound import *

def initialize():
    # Create all the variables.
    global audioData
    audioData = AudioData()


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, title=title, size=(300,300))
        initialize()
        global menuSave, menuPlay, soundfile, audioData, menuAudioProcess
        global sounddirectory, tRecord, tTunning, menuPlayMidi
        panel = wx.Panel(self)

        # Setting up the menu.
        filemenu = wx.Menu()
        soundmenu = wx.Menu()
        helpmenu = wx.Menu()

        # Creating the items in the menu
        # --- File menu ---
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file")
        menuSave = filemenu.Append(wx.ID_SAVE, "Save", "Save file")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        menuSave.Enable(False)


        # --- Sound menu ---
        menuRecord = soundmenu.Append(wx.ID_ANY, "&Record", "Record an audio")
        menuPlay = soundmenu.Append(wx.ID_ANY, "Play", "Play an audio")
        menuAudioProcess = soundmenu.Append(wx.ID_ANY, "Generate PDF", "Generate PDF from audio")
        menuPlayMidi = soundmenu.Append(wx.ID_ANY, "Play MIDI", "Play MIDI")
        menuPlay.Enable(False)
        menuAudioProcess.Enable(False)
        menuPlayMidi.Enable(False)

        # --- Help menu ---
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 
        menuBar.Append(soundmenu, "&Sound")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events of the menubar.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnRecord, menuRecord)
        self.Bind(wx.EVT_MENU, self.OnPlay, menuPlay)
        self.Bind(wx.EVT_MENU, self.OnAudioProcess, menuAudioProcess)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnPlayMidi, menuPlayMidi)


        # Creating the toolbar
        vbox = wx.BoxSizer(wx.VERTICAL)
        global mainToolbar
        mainToolbar = wx.ToolBar(self)
        toolbarOpen = mainToolbar.AddLabelTool(wx.ID_OPEN, '', wx.Bitmap(music_score_creator.__path__[0] + '/images/open32.png'))
        toolbarSave = mainToolbar.AddLabelTool(wx.ID_SAVE, '', wx.Bitmap(music_score_creator.__path__[0] + '/images/save32.png'))
        mainToolbar.AddSeparator()
        toolbarRecord = mainToolbar.AddLabelTool(5990, '', wx.Bitmap(music_score_creator.__path__[0] + '/images/record32.png'))
        toolbarPlay = mainToolbar.AddLabelTool(6001, '', wx.Bitmap(music_score_creator.__path__[0] + '/images/play32.png'))
        mainToolbar.AddSeparator()
        toolbarAudioProcess = mainToolbar.AddLabelTool(6002, '', wx.Bitmap(music_score_creator.__path__[0] + '/images/pdf32.png'))
        toolbarPlayMidi = mainToolbar.AddLabelTool(6003, '', wx.Bitmap(music_score_creator.__path__[0] + '/images/play32.png'))
        mainToolbar.EnableTool(wx.ID_SAVE, False) # Before we have an audio, it's deactivated.
        mainToolbar.EnableTool(6001, False)
        mainToolbar.EnableTool(6002, False)
        mainToolbar.EnableTool(6003, False)
        mainToolbar.Realize()

        # Set events of the toolbar

        self.Bind(wx.EVT_MENU, self.OnOpen, toolbarOpen)
        self.Bind(wx.EVT_MENU, self.OnRecord, toolbarRecord)
        self.Bind(wx.EVT_MENU, self.OnPlay, toolbarPlay)
        self.Bind(wx.EVT_MENU, self.OnAudioProcess, toolbarAudioProcess)
        self.Bind(wx.EVT_MENU, self.OnSave, toolbarSave)
        self.Bind(wx.EVT_MENU, self.OnPlayMidi, toolbarPlayMidi)

        vbox.Add(mainToolbar, 0, wx.EXPAND)

        # 
        tempos = ['60', '90', '120', '150']
        wx.StaticText(self, label=("Tempo"), pos=(10, 74))
        cb_tempo = wx.ComboBox(self, value=('60'), pos=(209, 70), size=(80, 28), choices=tempos, 
            style=wx.CB_READONLY)

        wx.StaticLine(self, pos=(0, 50), size=(300,1))

        tRecord = wx.TextCtrl(self,-1, pos=(209, 110), value="2")
        wx.StaticText(self, label=("Recording time (seconds)"), pos=(10, 114))
        #wx.StaticText(self, label=("seconds"), pos=(210, 114))

        measures = ['2/4', '3/4', '4/4']
        wx.StaticText(self, label=("Measure"), pos=(10, 154))
        cb_measure = wx.ComboBox(self, value=('4/4'), pos=(209, 150), size=(80, 28), choices=measures, 
            style=wx.CB_READONLY)

        tTunning = wx.TextCtrl(self, -1, pos=(209, 190), value="440")
        wx.StaticText(self, label=("Tunning"), pos=(10, 194))

        cb_midi = wx.CheckBox(self, label="Generate MIDI", pos=(10, 234))


        # Events of the block

        self.Bind(wx.EVT_COMBOBOX, self.OnTempo, cb_tempo)
        self.Bind(wx.EVT_COMBOBOX, self.OnMeasure, cb_measure)
        self.Bind(wx.EVT_CHECKBOX, self.OnMidi, cb_midi)
        #self.Bind(wx.Ev)

        self.SetSizer(vbox)

        self.Show(True)

    def OnOpen(self, e):
        global soundfile, audioData, sounddirectory
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.wav", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            sounddirectory = self.dirname+"/"+self.filename
            soundfile = wave.open(self.dirname+"/"+self.filename, 'rb')
            mainToolbar.EnableTool(wx.ID_SAVE, True)
            mainToolbar.EnableTool(6001, True)
            mainToolbar.EnableTool(6002, True)
            menuSave.Enable(True)
            menuPlay.Enable(True)
            menuAudioProcess.Enable(True) 
            
        dlg.Destroy()

    def OnRecord(self, e):
        global soundfile,menuSave, menuPlay, menuAudioProcess, audioData, sounddirectory
        global tRecord
        mainToolbar.EnableTool(5990, False)
        time.sleep(3)
        audioData.record_seconds = int(tRecord.GetValue())
        (soundfile, frames, sounddirectory) = record(audioData)
        audioData.frames = frames
        mainToolbar.EnableTool(5990, True)
        mainToolbar.EnableTool(wx.ID_SAVE, True)
        mainToolbar.EnableTool(6001, True)
        mainToolbar.EnableTool(6002, True)
        menuSave.Enable(True)
        menuPlay.Enable(True)
        menuAudioProcess.Enable(True)

    def OnAudioProcess(self, e):
        #Add interaction to save the file. In test, only the path to the file to process
        global sounddirectory, tTunning, audioData, menuPlayMidi
        audioData = updateConversionList(audioData, int(tTunning.GetValue()))
        audioProcessing(sounddirectory, audioData)
        if audioData.midi == 1:
            mainToolbar.EnableTool(6003, True)
            menuPlayMidi.Enable(True)
        if audioData.midi == 0:
            mainToolbar.EnableTool(6003, False)
            menuPlayMidi.Enable(False)

    def OnSave(self, e):
        global soundfile, audioData
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Save audio", self.dirname, "", "*.wav", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            save(self.dirname, self.filename, soundfile, audioData)
        dlg.Destroy()

    def OnAbout(self, e):
        dlg = wx.MessageDialog( self, "An attempt of doing a music score creator.\nVersion 0.8beta - 2014\nCreated by Jose Carlos M. Aragon.\nYou can contact me via twitter: @Montagon.", "About Music score creator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPlay(self, e):
        global soundfile, audioData, sounddirectory
        play(soundfile, audioData, sounddirectory)

    def OnExit(self, e):
        self.Close(True)

    def OnTempo(self, e):
        global audioData
        audioData.quarter_note_minute = int(e.GetString())

    def OnMeasure(self, e):
        global audioData
        audioData.measure = e.GetString()

    def OnMidi(self, e):
        global audioData
        sender = e.GetEventObject()
        isChecked = sender.GetValue()

        if isChecked:
            audioData.midi = 1
        else:
            audioData.midi = 0

    def OnPlayMidi(self, e):
        global audioData
        pygame.mixer.init(audioData.rate, audioData.format, audioData.channels, audioData.chunk)
        pygame.mixer.music.load("score.midi")
        pygame.mixer.music.play()


app = wx.App(False)
frame = MainWindow(None, "Music score creator")
app.MainLoop()