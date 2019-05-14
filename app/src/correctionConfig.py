#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:57:45 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel
from myLineEdit import MyLineEdit

class CorrectionConfig(QWidget):
    '''
    Panel where the user can decide the Correction parameters of the acquisition if he wants to use some
    Has default parameters
    Inherits from QWidget
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        # Possible values for Correction stream configuration
        corr_flag = False
        corr_type=(['NTRIP Client','TCP Client'])
        corr_index_type=0
        corr_format=(['RTCM2','RTCM3','BINEX','UBX'])
        corr_index_format=1
        corr_user = 'eleves'
        corr_addr = 'rgp-ip.ign.fr'
        corr_port = '2101'
        corr_pw = 's3YfJx54C7'
        corr_mp = 'TRS'
        
        self.corr_b = QCheckBox("Enable",self) ## see if possible to deactivate the other stuff

        
        self.type_list=QComboBox(self)
        self.type_list.addItems(corr_type)
        self.type_list.setCurrentIndex(corr_index_type)
        self.type_list.currentIndexChanged.connect(self.typeChanged)
        
        self.format_list=QComboBox(self)
        self.format_list.addItems(corr_format)
        self.format_list.setCurrentIndex(corr_index_format)

        self.corr_b.setChecked(corr_flag)
        self.addr_edit=MyLineEdit(corr_addr,self)
        self.port_edit=MyLineEdit(corr_port,self)
        self.mp_edit=MyLineEdit(corr_mp,self)
        self.user_edit=MyLineEdit(corr_user,self)
        self.pw_edit=MyLineEdit(corr_pw,self)

        # default activated parameters
        self.typeChanged(corr_index_type)

        ###### SETTING THE LAYOUT  #######
        
        grid=QGridLayout()
        grid.addWidget(self.corr_b,0,0)
        grid.addWidget(QLabel('Type/Format'),0,1)
        grid.addWidget(self.type_list,0,2)
        grid.addWidget(self.format_list,0,3)
        grid.addWidget(QLabel('Address'),1,0)
        grid.addWidget(self.addr_edit,1,1,1,4)
        grid.addWidget(QLabel('Port'),2,0)
        grid.addWidget(self.port_edit,2,1)
        grid.addWidget(QLabel('Mountpoint'),2,2)
        grid.addWidget(self.mp_edit,2,3)
        grid.addWidget(QLabel('User-ID'),3,0)
        grid.addWidget(self.user_edit,3,1)
        grid.addWidget(QLabel('Password'),3,2)
        grid.addWidget(self.pw_edit,3,3)
        self.setLayout(grid)

        

    def typeChanged(self,ind):
        '''
        Check wether TCP or NTRIP is chosen for correction and activate/deactivate corresponding parameters
        arg ind : int (index of the corr_type parameter)
        '''
        if ind==0: # TCP Client
            self.mp_edit.setDisabled(False)
            self.user_edit.setDisabled(False)
            self.pw_edit.setDisabled(False)
        elif ind==1: # NTRIP Client
            self.mp_edit.setDisabled(True)
            self.user_edit.setDisabled(True)
            self.pw_edit.setDisabled(True)
            

        