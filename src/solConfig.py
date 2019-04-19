#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:42:29 2019

@author: edgar
"""

import glob, os
from time import gmtime, strftime

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel

from myLineEdit import MyLineEdit

class SolConfig(QWidget):
    '''
    Panel where the user can decide wether to save or not the solutions files
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
        sol_flag = True
        
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        self.__dir = glob.glob('/media/') #search for the USB memory
        print(type(dir))
        if (len(self.__dir)==0): #if not found, save in the specified solution directory  
            print("ok")
            self.__dir = [self.__dirtrs +'/Solutions/']
            
        sol_filename = self.__dir[0]+ strftime('%Y-%m-%d %H:%M:%S',gmtime()) + '.pos'  #file name as year-month-day hour:minute:second in UTC


        # Setting the elements on the layout
        self.sol_b = QCheckBox("Enable",self)
        self.sol_b.setChecked(sol_flag)
        
        self.output_edit=MyLineEdit(sol_filename)

        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(self.sol_b,0,0)
        grid.addWidget(QLabel('Output File name'),1,0)
        grid.addWidget(self.output_edit,1,1)
        self.setLayout(grid)