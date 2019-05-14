#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:13:49 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel
from myLineEdit import MyLineEdit
from subprocess import check_output
from functools import partial

class OutputConfig(QWidget):
    '''
    Panel where the user can decide if he wants the output of the base acquisition to be sent to the rover through 
    a cloud (NTRIP or TCP)
    If yes, the user can set the parameters for the connection to the caster
    Has default parameters
    Inherits from QWidget
    
    Parameters:
        Core :
            private Boolean output_flag : wether the output shall be transmited through a cloud
            private list output_type : choose between NTRIP and TCP protocol
            private int output_index_type
            private liste output_format : wich format shall be applied (rtcm or ubx)
            private int output_index_format
            private String output_user : gives the user name to connect with
            private String output_addr : gives the cloud address to connect to
            private String output_port : gives the port to connect to
            private String output_pw : gives the password to connect with
            private String output_mp : gives the mountpoint to connect to
        UI :
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
        self.__output_flag = False
        self.__output_type=(['tcpcli','ntripcli'])
        self.__output_index_type = 1
        self.__output_format=(['ubx','rtcm3'])
        self.__output_index_format = 0
        self.__output_user = 'eleves'
        self.__output_addr = 'rgp-ip.ign.fr'
        self.__output_port = '2101'
        self.__output_pw = 's3YfJx54C7'
        self.__output_mp = 'FORC2'


        # Setting the elements on the layout
        self.__output_b = QCheckBox("Enable",self)
        self.__output_b.setChecked(self.__output_flag)
        
        self.__type_list=QComboBox(self)
        self.__type_list.addItems(['TCP Server','NTRIP Server'])
        self.__type_list.setCurrentIndex(self.__output_index_type)
        
        self.__format_list=QComboBox(self)
        self.__format_list.addItems(['UBX','RTCM3'])
        self.__format_list.setCurrentIndex(self.__output_index_format)
        
        self.__addr_edit=MyLineEdit(self.__output_addr,self)
        
        self.__port_edit=MyLineEdit(self.__output_port,self)
        
        self.__mp_edit=MyLineEdit(self.__output_mp,self)
        
        self.__user_edit=MyLineEdit(self.__output_user,self)
        
        self.__pw_edit=MyLineEdit(self.__output_pw,self)
        
        # default activated parameters
        self.typeChanged()
        self.__output_b.stateChanged.connect(partial(self.typeChanged))
        self.__type_list.currentIndexChanged.connect(self.typeChanged)
        



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
        

        
        ######  FUNCTIONS  #######

    def typeChanged(self):  
        '''
        Check the transmission type selected and disables/displays the corresponding
        parameters on the UI
        '''

        
        if self.__output_b.isChecked() == True:
            
            self.__type_list.setDisabled(False)  
            self.__format_list.setDisabled(False) 
            self.__port_edit.setDisabled(False)
            self.__addr_edit.setDisabled(False)
           
            
            if self.__type_list.currentIndex() == 0: # TCP Server
                
                self.__addr_edit.setText(self.getIpAddress())
                self.__output_addr = self.getIpAddress()
                self.__mp_edit.setDisabled(True)
                self.__user_edit.setDisabled(True)
                self.__pw_edit.setDisabled(True)

                
            if self.__type_list.currentIndex() == 1: # NTRIP Server
                
                self.__mp_edit.setDisabled(False)
                self.__user_edit.setDisabled(False)
                self.__pw_edit.setDisabled(False)


                
        else:
            self.__type_list.setDisabled(True)  
            self.__format_list.setDisabled(True)   
            self.__addr_edit.setDisabled(True)
            self.__mp_edit.setDisabled(True)
            self.__user_edit.setDisabled(True)
            self.__pw_edit.setDisabled(True)
            self.__port_edit.setDisabled(True)
            


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
        
        
    
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''      

        self.__output_flag = self.__output_b.isChecked()
        self.__output_index_type = self.__type_list.currentIndex()
        self.__output_index_format = self.__format_list.currentIndex()
        self.__output_user = self.__user_edit.text()
        self.__output_addr = self.__addr_edit.text()
        self.__output_port = self.__port_edit.text()
        self.__output_pw = self.__pw_edit.text()
        self.__output_mp = self.__mp_edit.text()

        
        
    def getOptions(self):
        '''
        Returns Input options 
        '''
        
        self.apply()
        
        
        return (self.__output_flag,
                self.__output_type[self.__output_index_type],
                self.__output_format[self.__output_index_format], 
                self.__output_user,
                self.__output_addr,
                self.__output_port,
                self.__output_pw,
                self.__output_mp)