#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:13:49 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel
from myLineEdit import MyLineEdit
from subprocess import check_output

class OutputConfig(QWidget):
    '''
    Panel where the user can decide the Output parameters of acquisition
    Has default parameters
    Inherits from QWidget
    
    Parameters:
        private QCheckBox output_b
        private QComboBox type_list
        private QComboBox format_list
        private MyLineEdit addr_edit
        private MyLineEdit mp_edit
        private MyLineEdit user_edit
        private MyLineEdit pw_edit
        
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        
        # Default Input stream configuration
        output_flag = False
        output_type=(['TCP Server','NTRIP Server','NTRIP Caster'])
        output_index_type=1
        output_format=(['UBX','RTCM3'])
        output_index_format=0
        output_user = 'eleves'
        output_addr = 'rgp-ip.ign.fr'
        output_port = '2101'
        output_pw = 's3YfJx54C7'
        output_mp = 'FORC2'


        # Setting the elements on the layout
        self.__output_b = QCheckBox("Enable",self)
        
        self.__type_list=QComboBox(self)
        self.__type_list.addItems(output_type)
        self.__type_list.setCurrentIndex(output_index_type)
        self.__type_list.currentIndexChanged.connect(self.typeChanged)
        
        self.__format_list=QComboBox(self)
        self.__format_list.addItems(output_format)
        self.__format_list.setCurrentIndex(output_index_format)

        self.__output_b.setChecked(output_flag)
        
        self.__addr_edit=MyLineEdit(output_addr,self)
        
        self.__port_edit=MyLineEdit(output_port,self)
        
        self.__mp_edit=MyLineEdit(output_mp,self)
        
        self.__user_edit=MyLineEdit(output_user,self)
        
        self.__pw_edit=MyLineEdit(output_pw,self)


        #Setting the Layout
        grid=QGridLayout()
        grid.addWidget(self.__output_b,0,0)
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
        self.typeChanged(output_index_type)
        
        
        ######  FUNCTIONS  #######

    def typeChanged(self,ind):  
        '''
        Check the transmission type selected and disables/displays the corresponding
        parameters on the UI
        '''
        if ind==0: # TCP Server
            self.__addr_edit.setText(self.getIpAddress())
            self.__addr_edit.setDisabled(True)
            self.__mp_edit.setDisabled(True)
            self.__user_edit.setDisabled(True)
            self.__pw_edit.setDisabled(True)
        if ind==1: # NTRIP Server
            self.__addr_edit.setText('élèves 666')   ###### to be changed !!!!!!!
            self.__addr_edit.setDisabled(False)
            self.__mp_edit.setDisabled(False)
            self.__user_edit.setDisabled(True)
            self.__pw_edit.setDisabled(False)
        if ind==2: # NTRIP Caster
            self.__addr_edit.setText(self.getIpAddress())
            self.__addr_edit.setDisabled(True)
            self.__mp_edit.setDisabled(False)
            self.__user_edit.setDisabled(False)
            self.__pw_edit.setDisabled(False)
        if ind==3: # Serial
            self.__addr_edit.setText(self.getIpAddress())
            self.__addr_edit.setDisabled(True)
            self.__mp_edit.setDisabled(False)
            self.__user_edit.setDisabled(False)
            self.__pw_edit.setDisabled(False)


    def getIpAddress(self):
        '''
        Return IP adress of the system
        
        returns:
            String IP address
            
        '''
        host=check_output(['hostname', '-I'])
        hosts=host.split()
        if len(hosts)==0:
            return '127.0.0.1'
        else:
            return hosts[0].decode()