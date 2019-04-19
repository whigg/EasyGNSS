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
    by a NTRIP-RTCM protocol 
    Inherits from QWidget
    
    Attributs:
        private QComboBox type_list
        private MyLineEdit lat_edit
        private MyLineEdit lon_edit
        private MyLineEdit hgt_edit
        
    !!!!!!! Might be cool to add a lat-long converter from decimal to deg-min-sec/cartesianne  !!!!!
    '''
    def __init__(self,parent=None):
        super().__init__()
        
        # Default Base position configuration
        basepos_type=(['LLH','RTCM'])
        basepos_index_type=0
        basepos_lat='48.8'
        basepos_lon='2.35'
        basepos_hgt='35'

        
        # Setting the elements on the layout
        self.__type_list=QComboBox(self)
        self.__type_list.addItems(basepos_type)
        self.__type_list.setCurrentIndex(basepos_index_type)
        self.__type_list.currentIndexChanged.connect(self.typeChanged)

        self.__lat_edit=MyLineEdit(basepos_lat)
        self.__lon_edit=MyLineEdit(basepos_lon)
        self.__hgt_edit=MyLineEdit(basepos_hgt)


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
        self.setLayout(grid)

        self.typeChanged(basepos_index_type)


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
        elif ind==1: # RTCM 
            self.__lat_edit.setDisabled(True)
            self.__lon_edit.setDisabled(True)
            self.__hgt_edit.setDisabled(True)