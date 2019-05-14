#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:38:50 2019

@author: edgar
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5 import QtCore

class TabSatellites(QDialog):
    '''
	This class hasn't been integrated to the code yet
    
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        
        
        self.label = 'N°Sat          Status L1          Azimuth          Elevation'
        self.satellites = 'Please start Rover acquisition first to show satellites'
        self.model = None
        
        self.setStyleSheet("background-color: rgb(161,183,36); font: 28pt 'Helvetica'; ")

        # Show the informations
        
        vboxs = QVBoxLayout()
        w1 = QLabel(self.label)
        w1.setAlignment(QtCore.Qt.AlignCenter)
        vboxs.addWidget(w1)
        w2 = QLabel(self.satellites)
        w2.setAlignment(QtCore.Qt.AlignCenter)
        vboxs.addWidget(w2)
        self.setLayout(vboxs)
        
    
    def setModel(self, model):
        '''
        '''
        self.model = model
        
    def updateSatellites(self):
        '''
        '''
        
        real_model = self.model.getInstanceRover()
        ls_sats = real_model.getSatellites()
        ls_sats = ls_sats.split('\n')
        
        del ls_sats[0:2]
        del ls_sats[-1]
        av_sats = ''
        sat = []
        if len(ls_sats) != 1:
            for ls_sat in ls_sats:
                sat = ls_sat.split(' ')
                av_sats = av_sats +str(sat[0])+'          '+str(sat[1])+'          '+str(sat[2])+'          '+str(sat[3]) + '\n'
        
        self.satellites.setText(av_sats)
