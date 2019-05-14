#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:57:16 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QFileDialog, QCheckBox, QLabel
import os
from time import gmtime, strftime
from myLineEdit import MyLineEdit
from functools import partial

class ConfConfig(QWidget):
    
    def __init__(self,parent=None):
        print(1)
        super().__init__()
        
        self.__save_conf_flag = True
        self.__conf_flag = False
        self.__filepath = None
        
        #directory where conf file are saved
        self.__directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/'
        
        #file name as year-month-day hour:minute:second in UTC
        self.__save_conf_filename = strftime('%Y-%m-%d_%H-%M-%S',gmtime()) + '.conf'
        
        
        
        # setting the elements on the layout
        self.__conf_b = QCheckBox("Enable",self)
        self.__conf_b.setChecked(self.__conf_flag)
        
        self.__save_conf_b = QCheckBox("Enable",self)
        self.__save_conf_b.setChecked(self.__save_conf_flag)
        
        self.__browse_b = QPushButton('Browse', self)
        self.__browse_b.clicked.connect(self.getfiles)
        
        self.__filename_edit = MyLineEdit(self.__save_conf_filename)
        
        
        
        # default activated parameters
        self.typeChanged()
        self.__conf_b.stateChanged.connect(partial(self.typeChanged))
        self.__save_conf_b.stateChanged.connect(partial(self.typeChanged))



        #setting the layout
        grid=QGridLayout()
        
        grid.addWidget(QLabel('Use existing conf file ?'),0,0)
        grid.addWidget(self.__conf_b,0,1)
        grid.addWidget(QLabel('Select the conf file to be used'),1,0)
        grid.addWidget(self.__browse_b,1,1)
        grid.addWidget(QLabel('Save created conf file ?'),2,0)
        grid.addWidget(self.__save_conf_b,2,1)
        grid.addWidget(QLabel('Filename'),3,0)
        grid.addWidget(self.__filename_edit,3,1)
        
        self.setLayout(grid)


    def getfiles(self):
        '''
        Opens the os file browser at the saved_conf/ directory
        Sets the filepath as the path to the selected file
        '''
        
        self.__filepath, _ = QFileDialog.getOpenFileName(self, 'Single File', self.__directory  , '*.conf')
        
        
        
    def typeChanged(self):
        '''
        Check wether the solution is enabled 
        '''
        # use existing conf file
        if self.__conf_b.isChecked() == True: 
            
            self.__browse_b.setDisabled(False)
            self.__save_conf_b.setChecked(False)
            self.__save_conf_b.setDisabled(True)
            self.__filename_edit.setDisabled(True)
            
        else:
            
            self.__browse_b.setDisabled(True)
            self.__save_conf_b.setDisabled(False)
            self.__filename_edit.setDisabled(False)
            
        # save creadted conf file   
        if self.__save_conf_b.isChecked() == True: 
            
            self.__filename_edit.setDisabled(False)
            
        else:
            
            self.__filename_edit.setDisabled(True)
            
            
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''
        
        self.__conf_flag = self.__conf_b.isChecked()
        self.__save_conf_flag = self.__save_conf_b.isChecked()
        self.__save_conf_filename = self.__filename_edit.text()
        
            
        
    def getOptions(self):
        '''
        Returns Solution options 
        '''
        
        self.apply()
        
        return (self.__conf_flag,
                self.__save_conf_flag,
                self.__filepath,
                self.__directory + self.__save_conf_filename)

