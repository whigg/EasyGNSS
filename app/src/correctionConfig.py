#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:57:45 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel
from myLineEdit import MyLineEdit
from functools import partial

class CorrectionConfig(QWidget):
    '''
    Panel where the user can set the parameters of the correction of a cloud (NTRIP or TCP) transmission from the base
    if he is using it. Otherwise he can disable it
    !!!! those parameters shall be equal to those set on the Output option for the base
    Has default parameters
    Inherits from QWidget
    
    Attributes:
        Core : 
            private Boolean corr_flag : wether correction from the base are transmitted to a NTRIP or TCP protocol 
            private list corr_type : wether it follows a NTRIP or TCP protocol
            private int corr_index_type
            private list corr_format : in wich format is it sent (rtcm or ubx)
            private int corr_index_format
            private String output_user : gives the user name to connect with
            private String output_addr : gives the cloud address to connect to
            private String output_port : gives the port to connect to
            private String output_pw : gives the password to connect with
            private String output_mp : gives the mountpoint to connect to
        UI : 
            private QCheckBox corr_b
            private QComboBox type_list
            private QComboBox format_list
            private MyLineEdit addr_edit
            private MyLineEdit port_edit
            private MyLineEdit mp_edit
            private MyLineEdit pw_edit
            private MyLineEdit user_edit
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        # Possible values for Correction stream configuration
        self.__corr_flag = False
        self.__corr_type=(['ntripcli','tcpcli'])
        self.__corr_index_type=0
        self.__corr_format=(['rtcm2','rtcm3','binex','ubx'])
        self.__corr_index_format=1
        self.__corr_user = 'user'
        self.__corr_addr = 'adresse.com'
        self.__corr_port = '2101'
        self.__corr_pw = 's3YfJx54C7'  
        self.__corr_mp = 'TRS'   #Mountpoint
        
        
        #Setting elements of the layout
        
        self.__corr_b = QCheckBox("Enable",self) 
        self.__corr_b.setChecked(self.__corr_flag)
        
 
        self.__type_list=QComboBox(self)
        self.__type_list.addItems(['NTRIP Client','TCP Client'])
        self.__type_list.setCurrentIndex(self.__corr_index_type)
        self.__type_list.currentIndexChanged.connect(self.typeChanged)
        
        self.__format_list=QComboBox(self)
        self.__format_list.addItems(['RTCM2','RTCM3','BINEX','UBX'])
        self.__format_list.setCurrentIndex(self.__corr_index_format)
        
        self.__addr_edit = MyLineEdit(self.__corr_addr,self)
        self.__port_edit = MyLineEdit(self.__corr_port,self)       
        self.__mp_edit = MyLineEdit(self.__corr_mp,self)
        self.__user_edit = MyLineEdit(self.__corr_user,self)
        self.__pw_edit = MyLineEdit(self.__corr_pw,self)
        
        # default activated parameters
        self.typeChanged()
        self.__corr_b.stateChanged.connect(partial(self.typeChanged))
        self.__type_list.currentIndexChanged.connect(self.typeChanged)
        
        
        
        ###### SETTING THE LAYOUT  #######
        
        grid=QGridLayout()
        grid.addWidget(self.__corr_b,0,0)
        grid.addWidget(QLabel('Type/Format'),0,1)
        grid.addWidget(self.__type_list,0,2)
        grid.addWidget(self.__format_list,0,3)
        grid.addWidget(QLabel('Address'),1,0)
        grid.addWidget(self.__addr_edit,1,1,1,4)
        grid.addWidget(QLabel('Port'),2,0)
        grid.addWidget(self.__port_edit,2,1)
        grid.addWidget(QLabel('Mountpoint'),2,2)
        grid.addWidget(self.__mp_edit,2,3)
        grid.addWidget(QLabel('User-ID'),3,0)
        grid.addWidget(self.__user_edit,3,1)
        grid.addWidget(QLabel('Password'),3,2)
        grid.addWidget(self.__pw_edit,3,3)
        self.setLayout(grid)

        

    def typeChanged(self):
        '''
        Check wether the correction is enabled 
        If yes, check wether TCP or NTRIP is chosen for correction and activate/deactivate corresponding parameters
        arg ind : int (index of the corr_type parameter)
        '''
        if self.__corr_b.isChecked() == True:   
            
            self.__type_list.setDisabled(False)
            self.__format_list.setDisabled(False)
            self.__addr_edit.setDisabled(False)
            self.__port_edit.setDisabled(False)
            
            if self.__type_list.currentIndex() == 0: # NTRIP Client
                self.__mp_edit.setDisabled(False)
                self.__user_edit.setDisabled(False)
                self.__pw_edit.setDisabled(False)
                
            elif self.__type_list.currentIndex() == 1: # TCP Client
                self.__mp_edit.setDisabled(True)
                self.__user_edit.setDisabled(True)
                self.__pw_edit.setDisabled(True)      
        else:
            self.__mp_edit.setDisabled(True)
            self.__user_edit.setDisabled(True)
            self.__pw_edit.setDisabled(True)
            self.__type_list.setDisabled(True)
            self.__format_list.setDisabled(True)
            self.__addr_edit.setDisabled(True)
            self.__port_edit.setDisabled(True)
            
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''
        
        self.__corr_flag = self.__corr_b.isChecked()
        self.__corr_index_type = self.__type_list.currentIndex()
        self.__corr_index_format = self.__format_list.currentIndex()
        self.__corr_addr = self.__addr_edit.text()
        self.__corr_port = self.__port_edit.text()      
        self.__corr_mp = self.__mp_edit.text()
        self.__corr_user = self.__user_edit.text()
        self.__corr_pw = self.__pw_edit.text()
            
    def getOptions(self):
        '''
        Returns Corrections options in a list
        '''
        
        self.apply()
        
        return (self.__corr_flag,
                self.__corr_type[self.__corr_index_type],
                self.__corr_format[self.__corr_index_format],
                self.__corr_user,
                self.__corr_pw,
                self.__corr_port,
                self.__corr_mp,
                self.__corr_addr)
        