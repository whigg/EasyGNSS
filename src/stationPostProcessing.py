#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:37:12 2019

@author: pc-apple
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QLabel, QCheckBox

from myLineEdit import MyLineEdit

class StationPostProcessing(QWidget):
    '''
    Panel where the user can decide the Input parameters of the acquisition
    Has default parameters
    Inherits from QWidget
    
    Attributes:
        public QComboBox port_list
        public QComboBox bitrate_list
        public QComboBox bytesize_list
        public QComboBox parity_list
        public QComboBox stopbits_list
        public QComboBox flowcontrol_list
        
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        default_nb = "3"
        default_dist = "100"
        
        # Possible values for Input stream configuration  
        choices = (["Choose the stations", "Let the application choose the stations (you can specify a maximum number of stations and a maximum distance)"])
        choices_index = 0
        
        self.__choices_list=QComboBox(self)
        self.__choices_list.addItems(choices)
        self.__choices_list.setCurrentIndex(choices_index)
        self.__choices_list.currentIndexChanged.connect(self.typeChanged)
        self.__nb_edit=MyLineEdit(default_nb)
        self.__dist_edit=MyLineEdit(default_dist)
        
        #Setting the Layout
        layout = QVBoxLayout()
        layout.addWidget(self.__choices_list)
        layout.addWidget(QLabel("Maximum number of stations:"))
        layout.addWidget(self.__nb_edit)
        layout.addWidget(QLabel("Maximum distance (km):"))
        layout.addWidget(self.__dist_edit)
        self.setLayout(layout)
        self.typeChanged(choices_index)


    def typeChanged(self,ind):
        '''
        Check wether manual or automatic base position is selected and leave access 
        to the following parameter
        
        Parameters:
            integer ind
        '''
        if ind==0: # Choose the stations
            self.__nb_edit.setDisabled(False)
            self.__dist_edit.setDisabled(False)
        elif ind==1: # Let the application choose the stations
            self.__nb_edit.setDisabled(True)
            self.__dist_edit.setDisabled(True)