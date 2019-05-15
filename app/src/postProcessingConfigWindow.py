#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:50:24 2019

@author: pc-apple
"""

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QDialog, QLabel, QSizePolicy, QDesktopWidget
from PyQt5 import QtCore

from optionPostProcessing import OptionPostProcessing
from stationPostProcessing import StationPostProcessing

class PostProcessingConfigWindow:
    '''
    Class RoverConfigWindow is a QDialog subwindow that opens when TabRover.__confi_b is clicked
    It contains all the changeable parameters for the acquisition sorted by type
    
    Attributtes:
        private QDialog window : the window created by the class
        private ConnectionToModel rover_model : accessor to the Rover Model
        private OptionPostProcessing tab_option : 
        private StationPostProcessing tab_station : 
        private QPushButton apply_b : apply and save the modified parameters
        private QPushButton close_b : close the config window
        
    '''
    def __init__(self, parent=None):
        
        self.__window = QDialog(parent)
        self.__parent = parent

        self.__window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        screenShape = QDesktopWidget().screenGeometry()

        self.__window.setGeometry(0, 0, int(screenShape.width()*1300/1366), int(screenShape.height()*500/768))
        string = "background-color: rgb(245, 190, 35); font: 25pt 'Helvetica';"
        self.__window.setStyleSheet(string)

        self.__postProcess_model = None
        
        ######  CONFIGURATION PART  ######
        tabs = QTabWidget()

        self.__tab_option = OptionPostProcessing()
        self.__tab_station = StationPostProcessing()
        
        tabs.addTab(self.__tab_option,"Options")
        tabs.addTab(self.__tab_station, "Stations")
        
        ######  BUTTONS  ######

        self.__apply_button= QPushButton('Apply')
        self.__apply_button.clicked.connect(self.applyParam)
    
        hbox = QHBoxLayout()
        hbox.addWidget(self.__apply_button)
        
        ######  SETTING GLOBAL LAYOUT ######
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        layout.addLayout(hbox)

        self.__window.setLayout(layout)
        
        
        
        
    ######  FUNCTIONS  #######
    
    
        
    def show(self):
        '''
        Show RoverConfigWindow on screen
        '''
        self.__window.exec_()
        
        
    def setModel(self, model):
        '''
        Setter of the model attribute
        '''
        self.__postProcess_model = model
        
    def applyParam(self):
        '''
        Apply the chosen parameters to the model
        
        The getOptions method for each classes returns the values of each option
        It is hard coded so obviously not incredible but I could not return a list of values as I'd like
        cause Python encodes the list
        This might be interessting to find another way round for future developpments
        '''

        (confpath, ubxpath, pospath, mode, output_format) = self.__tab_option.getOptions()

        (nb_station, dist_max) = self.__tab_station.getOptions()
        
        if confpath == None or ubxpath == None or pospath == None:
            self.problemApply()
            return
            
        print(confpath, ubxpath, pospath, mode, output_format, nb_station, dist_max)

        real_postProcess_model = self.__postProcess_model.getInstancePostProcess()
        real_postProcess_model.setOptions(confpath, ubxpath, pospath, mode, output_format, nb_station, dist_max)
        
        self.confirmApply()
        
        
    def confirmApply(self):
        '''
        Shows a small subwindow to confirm that parameters have been applied 
        It exits both config window and subwindow when 'OK' is pressed
        '''

        d = QDialog()
        screenShape = QDesktopWidget().screenGeometry()
        d.setGeometry(int(screenShape.width()*400/1366), int(screenShape.height()*300/768),int(screenShape.width()*200/1366), int(screenShape.height()*200/768))
        d.setWindowTitle('Parameters')
        
        label = QLabel('Parameters saved')
        
        b1 = QPushButton("ok",d)
        b1.clicked.connect(self.__window.close)
        b1.clicked.connect(d.close)
        b1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(b1)
        d.setLayout(layout)
        d.setStyleSheet("background-color: rgb(161,183,36); font: 24pt 'Helvetica'; ")
        
        d.exec_()
 
       
    def problemApply(self):
        
        
        d = QDialog()
        d.setGeometry(400,300,200,200)
        d.setWindowTitle('Parameters')
        
        label = QLabel('Please select a conf file, an ubx file AND a pos file')
        
        b1 = QPushButton("ok",d)
        b1.clicked.connect(d.close)
        b1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(b1)
        d.setLayout(layout)
        d.setStyleSheet("background-color: rgb(161,183,36); font: 24pt 'Helvetica'; ")
        
        d.exec_()