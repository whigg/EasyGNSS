#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:28:22 2019

@author: edgar

This script was originally made by Valentin in the previous ENSG-Géomatique project on low-cost GNSS 
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel


class Chronometer(QLabel):
    '''
    The Chronometer class sets up and displays a time-mesuring tool for the app
    Inherits from QLabel
    
    Attributes:
        int seconde 
        int minute
        int hour
    '''
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.tick)
        self.seconde = 0
        self.minute = 0
        self.hour = 0
        self.setText("Running for: \n 00:00:00")

        
    def start(self):
        '''
        Starts the chronometer
        '''
        self.seconde = 0
        self.minute = 0
        self.hour = 0        
        self.timer.start(1000)

    def tick(self):
        '''
        Updates the chronometer
        '''
        self.seconde+=1
        if self.seconde == 60:
            self.minute+=1
            self.seconde=0
            if self.minute == 60:
                self.hour+=1
                self.minute=0
        self.setText("Runnig for: \n {:02d}:{:02d}:{:02d}".format(self.hour,self.minute,self.seconde))
        
    def stop(self):
        '''
        Stops the chronometer
        '''
        self.timer.stop()