#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:55:14 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from myLineEdit import MyLineEdit


class BasePosConfig_Base(QWidget):
    '''
    Panel where the user can set the position of the base station for the base acquisition
    Inherits from QWidget
    
    Attributes:
        Core :
            private String basepos_lat : latitude of the base posiotion
            private String basepos_lon : longitude of the base position
            private String basepos_hgt : heigth of the base position
            private String basepos_ant_hgt : height of the base antenna
        UI :     
            private MyLineEdit lat_edit
            private MyLineEdit lon_edit
            private MyLineEdit hgt_edit
            private MyLineEdit ant_hgt_edit

    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        # Default Base position configuration
        self.__basepos_lat = '48.8'
        self.__basepos_lon = '2.35'
        self.__basepos_hgt = '35'
        self.__basepos_ant_hgt = '0'


        # Setting the elements on the layout
        self.__lat_edit=MyLineEdit(self.__basepos_lat)
        self.__lon_edit=MyLineEdit(self.__basepos_lon)
        self.__hgt_edit=MyLineEdit(self.__basepos_hgt)
        self.__ant_hgt_edit=MyLineEdit(self.__basepos_ant_hgt)

        #Setting the Layout
        grid=QGridLayout()
        
        grid.addWidget(QLabel('Latitude (deg)'),0,0)
        grid.addWidget(self.__lat_edit,0,1)
        
        grid.addWidget(QLabel('Longitude (deg)'),1,0)
        grid.addWidget(self.__lon_edit,1,1)
        
        grid.addWidget(QLabel('Height (m)'),2,0)
        grid.addWidget(self.__hgt_edit,2,1)
        
        grid.addWidget(QLabel('Antenna Height (m)'),3,0)
        grid.addWidget(self.__ant_hgt_edit,3,1)
        
        self.setLayout(grid)
        
    
    def apply(self):
        '''
        Changes values to the those selected in the UI
        '''

        self.__basepos_lat = self.__lat_edit.text()
        self.__basepos_lon= self.__lon_edit.text()
        self.__basepos_hgt= self.__hgt_edit.text()
        self.__basepos_ant_hgt = self.__ant_hgt_edit.text()
        
            
    def getOptions(self):
        '''
        Returns Base Position options 
        '''
        self.apply()
        
        return (self.__basepos_lat,
                self.__basepos_lon,
                self.__basepos_hgt,
                self.__basepos_ant_hgt)
        
        