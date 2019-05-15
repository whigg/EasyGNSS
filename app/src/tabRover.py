#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:57:52 2019

@author: edgar
"""

import os, re

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore

from chronometer import Chronometer
from roverConfigWindow import RoverConfigWindow
from connectionToModel import ConnectionToModel

class TabRover(QWidget):
    '''
    Class TabRover is the sub widget that contains the rover launch, 
    configuration and results for the rover
    Inherits from QWidget
    Divided into a Right Part, a Left Part, a Upper Part and a Lower Part
    
    Attributes:
        private path dirtrs : directory of the script
        private ConnectionToModel rover_model : connector to the Rover Model
        private QTimer rover_timer : timer of the widget
        private QPushButton start_b : button that launchs the acquisition
        private QPushButton config_b : button that opens the Config Window
        private QLabel icon : rover image
        private Chronometer chrono_rover : chronometer taht appears on the UI for the rover
        private QLabel lSol : indicates the mode of acquisition
        private QLabel lLong : shows the calculated Longitude
        private QLabel lLat : shows the calculated Latitude
        private QLabel lHeight : shows the calculated ellipsoidal Height
        private QLabel stream_status : shows the status of the stream
    
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        
        #Setting font
        self.setFont(QFont('Helvetica',25))
        # Get path to the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        #Connection to the Rover model
        self.__rover_model = ConnectionToModel()
        #timer
        self.__rover_timer = QtCore.QTimer(self)
        self.__rover_timer.timeout.connect(self.updateRover)  
        
        self.__satellites = None
           
        
        ######  RIGHT PART OF THE WIDGET  ######
        
        # Start Button
        self.__start_b = QPushButton('Start', self)
        self.__start_b.setCheckable(True)
        self.__start_b.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.__start_b.toggled.connect(self.startRover)
        
        # Config Button
        self.__config_b = QPushButton('Config', self)
        self.__config_b.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.__config_b.clicked.connect(self.openConfig)
               
        # Setting right part layout
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.__start_b)
        right_layout.addWidget(self.__config_b)
        
        
        ######  LEFT PART OF THE WIDGET  ######
        
        # Rover image
        fig = QPixmap(self.__dirtrs +'/img/rover.png')  
        self.__icon = QLabel(self)
        self.__icon.setPixmap(fig)
        
        # Chrono
        self.__chrono_rover = Chronometer()
        
        
        # Setting left part layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.__icon)
        left_layout.addWidget(self.__chrono_rover)
        
        
        ######  LOWER PART OF THE WIDGET  ######
        
        # Position indicators
        Sol_=QLabel('Sol:')
        Sol_.setAlignment(QtCore.Qt.AlignRight)
        Lat_=QLabel('Lat:')
        Lat_.setAlignment(QtCore.Qt.AlignRight)
        Lon_=QLabel('Lon:')
        Lon_.setAlignment(QtCore.Qt.AlignRight)
        Alt_=QLabel('Height:')
        Alt_.setAlignment(QtCore.Qt.AlignRight)
        
        # Calculated Position to be modified by updateRover()
        self.__lSol=QLabel('')       
        self.__lLat=QLabel('')      
        self.__lLon=QLabel('')       
        self.__lHeight=QLabel('')
        
        # Stream indicators
        status = QLabel('Stream Status:')
        status.setAlignment(QtCore.Qt.AlignLeft)
        self.__stream_status = QLabel('Not Started')
        self.__stream_status.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        
        
        # Setting lower part layout
        lower_layout = QHBoxLayout()
        
        lower_layout.addWidget(Sol_)
        lower_layout.addWidget(self.__lSol)
        lower_layout.addWidget(Lat_)
        lower_layout.addWidget(self.__lLat)
        lower_layout.addWidget(Lon_)
        lower_layout.addWidget(self.__lLon)
        lower_layout.addWidget(Alt_)
        lower_layout.addWidget(self.__lHeight)
        
        lower_layout2 = QHBoxLayout()
        lower_layout2.addWidget(status)
        lower_layout2.addWidget(self.__stream_status)
        
        ##### SETTING THE GLOBAL LAYOUT  ######
        
        rover_layout1 = QHBoxLayout()
        rover_layout1.addLayout(left_layout)
        rover_layout1.addLayout(right_layout)  
        
        rover_layout = QVBoxLayout()
        rover_layout.addLayout(rover_layout1)
        rover_layout.addLayout(lower_layout)
        rover_layout.addLayout(lower_layout2)
        self.setLayout(rover_layout)
        
        
        #################  FUNCTIONS  #########################
        
        
    def getModel(self):
        '''
        getter of the model
        return ConnectionToModel
        '''
        return self.__rover_model
    
    def passSatellites(self, satellites):
        '''
        passes the tabsatellites to connect to the rover timer
        '''
        self.__satellites = satellites

        
    def openConfig(self):
        '''
        Opens the RoverConfig subwindow
        '''
        try:
            # disabling buttons to prevent multi opennings and launchings
            self.__config_b.setDisabled(True)
            self.__start_b.setDisabled(True)
            
            subWindow = RoverConfigWindow(self)
            subWindow.setModel(self.__rover_model)
            subWindow.show()
            
        except Exception as e:
            print(e)
            
        # enabling buttons back
        self.__config_b.setDisabled(False)
        self.__start_b.setDisabled(False)
        
            
    def startRover(self):
        '''
        Launches the acquisition
        Notifies the Model
        Modifies the UI
        '''
        if self.__start_b.isChecked():    # if the acquisition is started
            
            try:
                # Notifying the model
                real_rover_model = self.__rover_model.getInstanceRover()
                real_rover_model.startRover()  
                
                # modifying the UI
                self.__start_b.setText('Stop')
                self.__config_b.setDisabled(True)
                
                self.__chrono_rover.start()
                self.__rover_timer.start(1000)
                
            except Exception as e:
                print(e)

        else:       # if the acquisition is stopped
            
            try:
                self.__rover_timer.stop()
                
                # Notifying the model
                real_rover_model = self.__rover_model.getInstanceRover()
                real_rover_model.stopRover()
                
                # modifying the UI
                self.__start_b.setText('Start')
                self.__config_b.setDisabled(False)
                
                self.__chrono_rover.stop()

                self.__lSol.setText('')
                self.__lLat.setText('')
                self.__lLon.setText('')
                self.__lHeight.setText('')
                self.__stream_status.setText('Not Started')
                
        
            except Exception as e:
                print(e)
        
        
    def updateRover(self):
        '''
        Access the Raws from the model and displays information on screen
        Displays the the calculus mode, the calculated position and the stream status 
        '''
        
        real_rover_model = self.__rover_model.getInstanceRover()
        rawsol, rawstream = real_rover_model.getRaw() 
               

        # solutions         
        if len(rawsol)>34:
            soltypes=re.findall(r'\(.*\)',rawsol)
            print(soltypes)
            
            try:
                soltype=soltypes[0][1:-1].strip()
                self.__lSol.setText(soltype)
                self.__lSol.setStyleSheet('font-family: Helvetica; font-size: 25pt')
                
            except Exception as e:
                print(e)
                sols=re.findall(r'\d*\.\d*',rawsol)
                print(sols)
                
            
                self.__lLat.setText(sols[1])
                self.__lLon.setText(sols[2])
                self.__lHeight.setText(sols[3])
                
            
        
        #stream
        rawstreams=rawstream.split('\n')

        statstr=''
        for stream in rawstreams:
            
            if stream.find('error')>0:
                streams=stream.split()
                statstr=streams[0]+' stream error'
                
            if stream.find(' C ')>0:
                streams=stream.split()
                if streams[0]=='input':
                    statstr=streams[1]+':'+streams[6]+'bps  '
                else:
                    statstr=streams[0]+':'+streams[8]+'bps  '
                    
        self.__stream_status.setText(statstr)
        

        
        
