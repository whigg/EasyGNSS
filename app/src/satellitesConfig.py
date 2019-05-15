# -*- coding: utf-8 -*-
"""
@author: BEILIN Jacques - IGN/ENSG
@date  : %(date)s
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel, QComboBox, QVBoxLayout
from myLineEdit import MyLineEdit

class SatellitesConfig(QWidget):
    '''
    public QCheckBox gps
    public QCheckBox glonass
    public QCheckBox galileo
    public QCheckBox beidou
    public QCheckBox qzss
    public QCheckBox sbas
    '''
    
    def __init__(self,parent=None):
        super().__init__()
        
        
        # Setting the elements on the layout
        self.gps = QCheckBox("GPS",self)
        self.gps.setChecked(True)
        self.glonass = QCheckBox("GLONASS",self)
        self.glonass.setChecked(False)
        self.galileo = QCheckBox("GALILEO",self)
        self.galileo.setChecked(False)
        self.beidou = QCheckBox("BEIDOU",self)
        self.beidou.setChecked(False)
        self.qzss = QCheckBox("QZSS",self)
        self.qzss.setChecked(False)
        self.sbas = QCheckBox("SBAS",self)
        self.sbas.setChecked(False)
    


        # Setting the layout
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Satellites System'))
        
        grid = QGridLayout()
        grid.addWidget(self.gps,2,0)
        grid.addWidget(self.glonass,2,1)
        grid.addWidget(self.galileo,2,2)
        grid.addWidget(self.beidou,3,0)
        grid.addWidget(self.qzss,3,1)
        grid.addWidget(self.sbas,3,2)
        vbox.addLayout(grid)
        
        self.setLayout(vbox)
        
        
    def getSatellites(self):
        '''
        Calculates the value corresponding to the satellites systems to be used as implemented in RTKLIB
        '''
        number = 0
        if self.gps.isChecked():
            number+=1
        if self.sbas.isChecked():
            number+=2
        if self.glonass.isChecked():
            number+=4
        if self.galileo.isChecked():
            number+=8
        if self.qzss.isChecked():
            number+=16
        if self.qzss.isChecked():
            number+=32
            
        return str(number)
    
    
    def getOptions(self):
        '''
        Returns Satellites options in a list
        '''
    
        return(self.getSatellites())