#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:47:54 2019

@author: pc-apple
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QPushButton, QFileDialog
import os

class OptionPostProcessing(QWidget):
    '''
    
    
    Attributes:
        
        
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        self.__directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/'
        self.__directory2 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/Results/Logs/'
        self.__directory3 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/Results/Solutions/'
        
        # Possible values for configuration
        self.__input_mode = (["static", "kinematic"])
        self.__output_format = (["xyz", "llh"])
        self.__confpath = None
        self.__pospath = None
        self.__ubxpath = None
        
        # Default configuration
        self.__input_index_mode = 0
        self.__output_index_format = 0

        # Setting the elements on the layout
        self.mode_list=QComboBox(self)
        self.mode_list.addItems(['Static','Kinematic'])
        self.mode_list.setCurrentIndex(self.__input_index_mode)

        self.format_list=QComboBox(self)
        self.format_list.addItems(['XYZ','LLH'])
        self.format_list.setCurrentIndex(self.__output_index_format)
        
        self.__browse_conf = QPushButton('Browse', self)
        self.__browse_conf.clicked.connect(self.getConfFiles)
        
        self.__browse_ubx = QPushButton('Browse', self)
        self.__browse_ubx.clicked.connect(self.getUbxFiles)
        
        self.__browse_pos = QPushButton('Browse', self)
        self.__browse_pos.clicked.connect(self.getPosFiles)

        #Setting the Layout
        layout = QGridLayout()
        layout.addWidget(QLabel('Conf file to be used'),0,0)
        layout.addWidget(self.__browse_conf,0,1)
        layout.addWidget(QLabel('UBX file to be used'),1,0)
        layout.addWidget(self.__browse_ubx,1,1)
        layout.addWidget(QLabel('Pos file to be used'),2,0)
        layout.addWidget(self.__browse_pos,2,1)
        layout.addWidget(QLabel('Calculus mode'),3,0)
        layout.addWidget(self.mode_list,3,1)
        layout.addWidget(QLabel('Output format'),4,0)
        layout.addWidget(self.format_list,4,1)
        self.setLayout(layout)
      
    
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''

        self.__input_index_mode = self.mode_list.currentIndex()
        self.__output_index_format = self.format_list.currentIndex()
        
    
    def getOptions(self):
        '''
        Returns options 
        '''
        
        self.apply()
        
        return(self.__confpath,
               self.__ubxpath,
               self.__pospath,
                self.__input_mode[self.__input_index_mode],
               self.__output_format[self.__output_index_format])
    
    def getConfFiles(self):
        '''
        Opens the os file browser at the saved_conf/ directory
        Sets the filepath as the path to the selected file
        '''
        
        self.__confpath, _ = QFileDialog.getOpenFileName(self, 'Single File', self.__directory  , '*.conf')
        
    def getUbxFiles(self):
        '''
        Opens the os file browser at the saved_conf/ directory
        Sets the filepath as the path to the selected file
        '''
        
        self.__ubxpath, _ = QFileDialog.getOpenFileName(self, 'Single File', self.__directory2  , '*.ubx')
        
    def getPosFiles(self):
        '''
        Opens the os file browser at the saved_conf/ directory
        Sets the filepath as the path to the selected file
        '''
        
        self.__pospath, _ = QFileDialog.getOpenFileName(self, 'Single File', self.__directory3  , '*.pos')