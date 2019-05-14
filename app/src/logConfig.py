#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:46:38 2019

@author: edgar
"""


import os
from time import gmtime, strftime
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel
from functools import partial
from myLineEdit import MyLineEdit

class LogConfig(QWidget):
    '''
    Panel where the user can decide wether to save or not the log files
    Inherits from QWIdget
    
    Attributes:
        Core : 
            private Boolean log_flag : wether logs shall be saved or not
            private String log_filename : name of the file where logs shall be saved
            private String logDirectory : path of the file where logs shall be saved
        UI :
            private QCheckBox log_b
            private MyLineEdit output_edit
    
    '''
    def __init__(self,parent=None):
        super().__init__()
        

        self.__log_flag = True
        
        dirtrs = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))     
        self.__logDirectory = dirtrs +'/Results/Logs/'         
        self.__log_filename =  strftime('%Y-%m-%d_%H-%M-%S',gmtime()) + '.ubx'  #file name as year-month-day hour:minute:second in UTC


        # Setting the elements on the layout
        self.__log_b = QCheckBox("Enable",self)
        self.__log_b.setChecked(self.__log_flag)
        
        self.__output_edit=MyLineEdit(self.__log_filename)
   
     
        # default activated parameters
        self.typeChanged()
        self.__log_b.stateChanged.connect(partial(self.typeChanged))


        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(self.__log_b,0,0)
        grid.addWidget(QLabel('Output File name'),1,0)
        grid.addWidget(self.__output_edit,1,1)
        self.setLayout(grid)
        
        
    def typeChanged(self):
        '''
        Check wether the log is enabled 
        '''
        
        if self.__log_b.isChecked() == True: 
            self.__output_edit.setDisabled(False)
            
        else:
            self.__output_edit.setDisabled(True)
            
    
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''
        
        self.__log_flag = self.__log_b.isChecked()
        self.__log_filename = self.__output_edit.text()
        
        
    def getOptions(self):
        '''
        Returns Logs options 
        '''
        
        self.apply()
        
        return (self.__log_flag, 
                self.__logDirectory + self.__log_filename)