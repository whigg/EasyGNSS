#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:21:26 2019

@author: edgar
"""

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QSizePolicy, QDialog

class InfoPostProcess(QDialog):
    '''
    Class that shows a subwindow when the post processing is launched
    And another one when it is completed
    
    Attributes : 
        public QLabel label
        public QPushButton quit_b
        public QVBoxLayout layout
    '''
    
    def __init__(self):
        
        # Inherits from the QDialog class
        super().__init__()
    
        self.setGeometry(400,300,200,200)
        self.setWindowTitle('Post Processing')
        
        self.label = QLabel('Post Processing in progress' + '\n' + 
                            'Please close this window and wait' + 
                            '\n It may take several minutes')
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: rgb(161,183,36); font: 24pt 'Helvetica'; ")
        
        
        
    def update(self):
        '''
        '''
        
        self.label.setText('Post Processing Done')

        
    def show(self):
        
        self.exec_()