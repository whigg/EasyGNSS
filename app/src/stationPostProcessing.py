#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:37:12 2019

@author: pc-apple
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from myLineEdit import MyLineEdit

class StationPostProcessing(QWidget):
    '''
        
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        
        # Possible values for Input stream configuration  
        self.__number = 3
        self.__dist = 100
        

        self.nb_edit=MyLineEdit("3")
        self.dist_edit=MyLineEdit("100")
        
        #Setting the Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Maximum number of stations:"))
        layout.addWidget(self.nb_edit)
        layout.addWidget(QLabel("Maximum distance (km):"))
        layout.addWidget(self.dist_edit)
        self.setLayout(layout)

        
    
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''

        self.__number = int(self.nb_edit.text())
        self.__dist = int(self.dist_edit.text())
        
    
    def getOptions(self):
        '''
        Returns options 
        '''
        
        self.apply()
        
        return(self.__number,
               self.__dist)

