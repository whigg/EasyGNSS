#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:54:39 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel

from myLineEdit import MyLineEdit

class BasePosConfig_Rover(QWidget):
    '''
    Panel where the user can set the position of the base station or ask to get it automatically
    by a RTCM protocol 
    Inherits from QWidget
    
    Attributs:
        Core : 
            private list basepos_type : see if the base position is transmitted from the the base (radio or cloud in rtcm)
            or if it shall be manually implemented
            private int basepos_index_type
            private String basepos_lat : latitude of the base posiotion
            private String basepos_lon : longitude of the base position
            private String basepos_hgt : heigth of the base position
            private String basepos_ant_hgt : height of the base antenna
        UI :     
            private QComboBox type_list
            private MyLineEdit lat_edit
            private MyLineEdit lon_edit
            private MyLineEdit hgt_edit
            private MyLineEdit ant_hgt_edit
        
    '''
    def __init__(self,parent=None):
        super().__init__()
        
        # Default Base position configuration
        self.__basepos_type = (['llh','rtcm'])
        self.__basepos_index_type = 1
        self.__basepos_lat = '48.8'
        self.__basepos_lon = '2.35'
        self.__basepos_hgt = '35'
        self.__basepos_ant_hgt = '0'

        
        # Setting the elements on the layout
        self.__type_list = QComboBox(self)
        self.__type_list.addItems(['LLH','RTCM'])
        self.__type_list.setCurrentIndex(self.__basepos_index_type)
        self.__type_list.currentIndexChanged.connect(self.typeChanged)

        self.__lat_edit = MyLineEdit(self.__basepos_lat)
        self.__lon_edit = MyLineEdit(self.__basepos_lon)
        self.__hgt_edit = MyLineEdit(self.__basepos_hgt)
        self.__ant_hgt_edit = MyLineEdit(self.__basepos_ant_hgt)


        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(QLabel('Base Position Type'),0,0)
        grid.addWidget(self.__type_list,0,1)
        grid.addWidget(QLabel('Latitude (deg)'),1,0)
        grid.addWidget(self.__lat_edit,1,1)
        grid.addWidget(QLabel('Longitude (deg)'),2,0)
        grid.addWidget(self.__lon_edit,2,1)
        grid.addWidget(QLabel('Height (m)'),3,0)
        grid.addWidget(self.__hgt_edit,3,1)
        grid.addWidget(QLabel('Antenna Height (m)'),4,0)
        grid.addWidget(self.__ant_hgt_edit,4,1)
        self.setLayout(grid)

        self.typeChanged(self.__basepos_index_type)


    def typeChanged(self,ind):
        '''
        Check wether manual or automatic base position is selected and leave access 
        to the following parameter
        
        Parameters:
            integer ind
        '''
        if ind==0: # LLH
            self.__lat_edit.setDisabled(False)
            self.__lon_edit.setDisabled(False)
            self.__hgt_edit.setDisabled(False)
            self.__ant_hgt_edit.setDisabled(False)
        elif ind==1: # RTCM 
            self.__lat_edit.setDisabled(True)
            self.__lon_edit.setDisabled(True)
            self.__hgt_edit.setDisabled(True)
            self.__ant_hgt_edit.setDisabled(True)
            
    def apply(self):
        '''
        Changes values to the those selected in the UI
        '''

        self.__basepos_index_type = self.__type_list.currentIndex()
        self.__basepos_lat = self.__lat_edit.text()
        self.__basepos_lon= self.__lon_edit.text()
        self.__basepos_hgt= self.__hgt_edit.text()
        self.__basepos_ant_hgt = self.__ant_hgt_edit.text()
        
            
    def getOptions(self):
        '''
        Returns Base Position options in a list
        '''
        self.apply()
        
        return (self.__basepos_type[self.__basepos_index_type],
                self.__basepos_lat,
                self.__basepos_lon,
                self.__basepos_hgt,
                self.__basepos_ant_hgt)