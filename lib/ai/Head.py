'''
Created on 5 avr. 2018

@author: AYB
'''
#! /usr/bin/python

#
# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import sys
import os.path
from lib.ai import vlc
from PyQt4 import QtGui, QtCore
from lib.ai.config  import Config
from time import sleep

class Head(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    CONFIG = Config()
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("AVA")
        self.CONFIG= Config()

        # creating a basic vlc instance
        self.instance = vlc.Instance('--input-repeat=999999 ') #--video-filter=transform --transform-type=270
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.showFullScreen()
        self.widget.setStyleSheet("background-color: black;")
        

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setStyleSheet("border-image: url(back.JPG); ")
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.widget.setLayout(self.vboxlayout)

        Toolbar = QtGui.QToolBar()
        Toolbar.setIconSize(QtCore.QSize(1,200))
        Toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon|QtCore.Qt.AlignLeading) #<= Toolbuttonstyle
        Toolbar.setStyleSheet("QToolBar { background: blue; }")
        self.addToolBar(QtCore.Qt.LeftToolBarArea,Toolbar)
        
        exit_button = QtGui.QToolButton()
        exit_button.setToolTip("Exit")
        
        exit_button.setCheckable(True)
        exit_button.toggled.connect(self.closeEvent)
        Toolbar.addWidget(exit_button)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def closeEvent(self):
        #Your desired functionality here
        print('Close button pressed')
        sys.exit(0)
        
    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()
    def test(self, anime):
        self.media = self.instance.media_new(anime)
        self.mediaplayer.set_media(self.media)
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.mediaplayer.play()
        
        
        #=======================================================================
        i = 0
        while True:
            state = self.mediaplayer.get_state()
            print(state)
            QtCore.QCoreApplication.processEvents()
            i = i + 1
            print(i)
        #=======================================================================
            #===================================================================
            if i == 200000:
                print("next:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
                self.mediaplayer.pause()
                #self.media = self.instance.media_new(self.CONFIG.AVA_TALK_ANIME)
                self.mediaplayer.set_mrl(self.CONFIG.AVA_TALK_ANIME)
                self.mediaplayer.play()
            #===================================================================
            if i == 400000:
                print("next:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
                self.mediaplayer.pause()
                #self.media = self.instance.media_new(self.CONFIG.AVA_TALK_ANIME)
                self.mediaplayer.set_mrl(anime)
                self.mediaplayer.play()
    
    def set_motion(self, anime):
        self.media = self.instance.media_new(anime)
        self.mediaplayer.set_media(self.media)
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.mediaplayer.play()
        
    def process_events(self):
            QtCore.QCoreApplication.processEvents()
        
                
                
class AVA():
    CONFIG = Config()
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.head = Head()
        self.head.showFullScreen()                
        
    def set_motion(self, motion):
        self.head.set_motion(motion)
    def test(self, motion):
        self.head.test(motion)
    def process_events(self):
        self.head.process_events()
        #=======================================================================
        # while True:
        #     state = self.head.mediaplayer.get_state()
        #     #print(state)
        #     QtCore.QCoreApplication.processEvents()
        #=======================================================================

if __name__ == "__main__":
    ava = AVA()
    ava.set_motion(ava.CONFIG.AVA_STANDBY_ANIME)
    sleep(10)
    ava.set_motion(ava.CONFIG.AVA_TALK_ANIME)
    
    print(ava.CONFIG.AVA_STANDBY_ANIME)   

    #===========================================================================
    # if sys.argv[1:]:
    #     head.OpenFile(sys.argv[1])
    # sys.exit(app.exec_())
    #===========================================================================
