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
    Panel where the user can set the position of the base station  
    Inherits from QWidget
    
    Attributes:
        private MyLineEdit lat_edit
        private MyLineEdit lon_edit
        private MyLineEdit hgt_edit
    
    !!!!!!! Might be cool to add a lat-long converter from decimal to deg-min-sec/cartesianne  !!!!!
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        # Default Base position configuration
        basepos_lat='48.8'
        basepos_lon='2.35'
        basepos_hgt='35'


        # Setting the elements on the layout
        self.__lat_edit=MyLineEdit(basepos_lat)
        self.__lon_edit=MyLineEdit(basepos_lon)
        self.__hgt_edit=MyLineEdit(basepos_hgt)


        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(QLabel('Latitude (deg)'),0,0)
        grid.addWidget(self.__lat_edit,0,1)
        grid.addWidget(QLabel('Longitude (deg)'),1,0)
        grid.addWidget(self.__lon_edit,1,1)
        grid.addWidget(QLabel('Height (m)'),2,0)
        grid.addWidget(self.__hgt_edit,2,1)
        self.setLayout(grid)