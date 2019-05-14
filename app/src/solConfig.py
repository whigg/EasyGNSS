#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:42:29 2019

@author: edgar
"""

import os
from time import gmtime, strftime
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel, QComboBox
from myLineEdit import MyLineEdit
from functools import partial

class SolConfig(QWidget):
    '''
    Panel where the user can decide wether to save or not the solutions files
    And to wich format, type and location
    Inherits from QWIdget
    
    Attributes:
        Core :
            private Boolean sol_flag : wether solutions shall be saved or not
            private list sol_type : type of the coordinates in the solution file
            private int sol_index_type
            private list sol_mode : all or single lines in the solution file
            private int sol_index_mode
            private String sol_filename : name of the file where solutions shall be saved
            private String solDirectory : path of the file where solutions shall be saved
            private String sol_format : format of the solutions (llh,xyz,enu)
        UI : 
            private QCheckBox sol_b 
            private QComboBox type_list
            private QComboBox type_mode
            private MyLineEdit output_edit        
    '''
    def __init__(self,parent=None):
        super().__init__()
        
        
        self.__sol_flag = True
        
        dirtrs = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        
        self.__solDirectory = dirtrs +'/Results/Solutions/'
            
        #file name as year-month-day hour:minute:second in UTC
        self.__sol_filename = strftime('%Y-%m-%d_%H-%M-%S',gmtime()) + '.pos' 
        
        # Settings of the output solution file
        self.__sol_type = ['llh','xyz','enu']
        self.__sol_index_type = 1
        self.__sol_mode = ['all','single']
        self.__sol_index_mode = 0
        

        # Setting the elements on the layout
        self.__sol_b = QCheckBox("Enable",self)
        self.__sol_b.setChecked(self.__sol_flag)
        
        self.__type_list = QComboBox(self)
        self.__type_list.addItems(['LLH','XYZ','ENU'])
        self.__type_list.setCurrentIndex(self.__sol_index_type)
        
        self.__type_mode = QComboBox(self)
        self.__type_mode.addItems(['ALL','SINGLE'])
        self.__type_mode.setCurrentIndex(self.__sol_index_mode)
        
        self.__output_edit=MyLineEdit(self.__sol_filename)
        
        
        # default activated parameters
        self.typeChanged()
        self.__sol_b.stateChanged.connect(partial(self.typeChanged))
        

        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(self.__sol_b,0,0)
        grid.addWidget(QLabel('Coordinates type'),1,0)
        grid.addWidget(self.__type_list,1,1)
        grid.addWidget(QLabel('Coordinates format'),2,0)
        grid.addWidget(self.__type_mode,2,1)
        grid.addWidget(QLabel('Output File name'),3,0)
        grid.addWidget(self.__output_edit,3,1)
        self.setLayout(grid)
        
    
    def typeChanged(self):
        '''
        Check wether the solution is enabled 
        '''
        
        if self.__sol_b.isChecked() == True: 
            
            self.__type_list.setDisabled(False)
            self.__type_mode.setDisabled(False)
            self.__output_edit.setDisabled(False)

            
        else:
            
            self.__type_list.setDisabled(True)
            self.__type_mode.setDisabled(True)
            self.__output_edit.setDisabled(True)

        
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''
        
        self.__sol_flag = self.__sol_b.isChecked()
        self.__sol_index_type = self.__type_list.currentIndex()
        self.__sol_index_mode = self.__type_mode.currentIndex()
        self.__sol_filename = self.__output_edit.text()
        
            
        
    def getOptions(self):
        '''
        Returns Solution options 
        '''
        
        self.apply()

        
        return (self.__sol_flag,
                self.__sol_type[self.__sol_index_type],
                self.__sol_mode[self.__sol_index_mode],
                self.__solDirectory + self.__sol_filename)