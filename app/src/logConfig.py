#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:46:38 2019

@author: edgar
"""


import glob, os
from time import gmtime, strftime

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel

from myLineEdit import MyLineEdit

class LogConfig(QWidget):
    '''
    Panel where the user can decide wether to save or not the log files
    Inherits from QWIdget
    
    Attributes:
        private path dirtrs 
        private tab of path dir
        public QCheckBox sol_b
        public MyLineEdit output_edit
    
    '''
    def __init__(self,parent=None):
        super().__init__()
        
        # Default Solution stream configration
        log_flag = True
        
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        self.__dir = glob.glob('/media/') #search for the USB memory
        print(type(dir))
        if (len(self.__dir)==0): #if not found, save in the specified solution directory  
            print("ok")
            self.__dir = [self.__dirtrs +'/Logs/']
            
        log_filename = self.__dir[0]+ strftime('%Y-%m-%d %H:%M:%S',gmtime()) + '.ubx'  #file name as year-month-day hour:minute:second in UTC


        # Setting the elements on the layout
        self.log_b = QCheckBox("Enable",self)
        self.log_b.setChecked(log_flag)
        
        self.output_edit=MyLineEdit(log_filename)

        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(self.log_b,0,0)
        grid.addWidget(QLabel('Output File name'),1,0)
        grid.addWidget(self.output_edit,1,1)
        self.setLayout(grid)