#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:34:35 2019

@author: edgar
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel, QComboBox, QVBoxLayout
from myLineEdit import MyLineEdit

class CalculusConfig(QWidget):
    '''
    Panel where the user can decide the calculus modes of the rover acquisition 
    It is the most basic parameter to set
    Inherits from QWIdget
    
    Attributes:
        Core : 
            private list calculus_mode : the mode of the acquisition  and treatment (single, dgps, ppp...)
            private int calculus_index_mode
            private String ant_hgt : the height of the antenna
            private list iono : avalaible ionospheric correction 
            private int iono_index
            private list tropo : avalaible tropospheric correction
            private int tropo_index
            private list eph : type of satellites ephemerids used
            private String elv_mask : elevation mask in degrees
        UI :
            private QComboBox calculus_list
            private MyLineEdit ant_hgt_edit
            private QComboBox iono_list
            private QComboBox tropo_list
            private QComboBox eph_list
            private MyLineEdit elv_mask_edit
            
    '''
    def __init__(self,parent=None):
        super().__init__()
        
        
        self.__calculus_mode = ['single','dgps','kinematic','static','movingbase','fixed','ppp-kine','ppp-static','ppp-fixed']
        self.__calculus_index_mode = 1
        self.__ant_hgt = '0'
        self.__iono = ['off','brdc','sbas','dual-freq','est-stec','ionex-tec','qzs-brdc','qzs-lex','stec']
        self.__iono_index = 1
        self.__tropo = ['off','saas','sbas','est-ztd','est-ztdgrad','ztd']
        self.__tropo_index = 1
        self.__eph = ['brdc','brdc+sbas','brdc+ssrapc','brdc+ssrcom']
        self.__eph_index = 0
        self.__elv_mask = '15.0' #elevation mask in degrees
        
        
        # Setting the elements on the layout
        
        self.__calculus_list = QComboBox(self)
        self.__calculus_list.addItems(['SINGLE','DGPS','KINEMATIC','STATIC',
                                       'MOVING BASE','FIXED',
                                       'PPP KINEMATIC','PPP STATIC','PPP FIXED'])
        self.__calculus_list.setCurrentIndex(self.__calculus_index_mode)
        
        self.__iono_list = QComboBox(self)
        self.__iono_list.addItems(['OFF','BROADCAST','SBAS','DUAL FREQ','EST-STEC','IONEX-TEC','QZS-BDRC',
                                   'QZS-LEX','STEC'])
        self.__iono_list.setCurrentIndex(self.__iono_index)
        
        self.__tropo_list = QComboBox(self)
        self.__tropo_list.addItems(['OFF','SAAS','SBAS','EST-ZTD','EST-ZTDGRAD','ZTD'])
        self.__tropo_list.setCurrentIndex(self.__tropo_index)
        
        self.__eph_list = QComboBox(self)
        self.__eph_list.addItems(['BROADCAST','BRDC+SBAS','BRDC+SSRAPC','BRDC+SSRCOM'])
        self.__eph_list.setCurrentIndex(self.__eph_index)
        
        self.__ant_hgt_edit = MyLineEdit(self.__ant_hgt)
        
        self.__elv_mask_edit = MyLineEdit(self.__elv_mask)
        
        
        # Setting the layout
        
        
        vbox = QVBoxLayout()
        grid1 = QGridLayout()
        
        grid1.addWidget(QLabel('Acquisition type'),0,0)
        grid1.addWidget(self.__calculus_list,0,1)
        grid1.addWidget(QLabel('Antenna height'),1,0)
        grid1.addWidget(self.__ant_hgt_edit,1,1)
        grid1.addWidget(QLabel('Ionospheric correction'),2,0)
        grid1.addWidget(self.__iono_list,2,1)
        grid1.addWidget(QLabel('Tropospheric correction'),3,0)
        grid1.addWidget(self.__tropo_list,3,1)
        grid1.addWidget(QLabel('Satellites ephemerids'),4,0)
        grid1.addWidget(self.__eph_list,4,1)
        grid1.addWidget(QLabel('Elevation Mask (deg)'),5,0)
        grid1.addWidget(self.__elv_mask_edit,5,1)
        
        vbox.addLayout(grid1)
              
        self.setLayout(vbox)
        
    
    
    
    def apply(self):
        '''
        Changes values to those selected in the UI
        '''
        self.__calculus_index_mode = self.__calculus_list.currentIndex()
        self.__ant_hgt = self.__ant_hgt_edit.text()
        self.__eph_index = self.__eph_list.currentIndex()
        self.__iono_index = self.__iono_list.currentIndex()
        self.__tropo_index = self.__tropo_list.currentIndex()
        self.__elv_mask = self.__elv_mask_edit.text()
        
    def getOptions(self):
        '''
        Returns Solution options in a list
        '''
        
        self.apply()

        return (self.__calculus_mode[self.__calculus_index_mode], 
                self.__ant_hgt,
                self.__iono[self.__iono_index],
                self.__tropo[self.__tropo_index],
                self.__eph[self.__eph_index],
                self.__elv_mask)