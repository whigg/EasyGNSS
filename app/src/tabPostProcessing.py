
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:46:17 2019
@author: nassim
"""

import os

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from postProcessingConfigWindow import PostProcessingConfigWindow
from connectionToModel import ConnectionToModel
from infoPostProcess import InfoPostProcess

class TabPostProcessing(QWidget):
    '''
    private String dirtrs : directory of the file
    private QPushButton start_b : button that launches the post processing
    private QPushButton config_b : button that opens the Config Window
    private QLabel icon : post processing image
    private ConnectionToModel postProcessing_model : connector to the Post Processing Model
    '''
    
    def __init__(self):
        
        # Inherits from the QWidget class
        super().__init__()
        
        #Setting font
        self.setFont(QFont('Helvetica',18))
        # Get path to the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))
        
        self.__postProcessing_model = ConnectionToModel()
        
        ######  RIGHT PART OF THE WIDGET  ######
        
        # Start Button
        self.__start_b = QPushButton('Start', self)
        self.__start_b.setCheckable(True)
        self.__start_b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.__start_b.toggled.connect(self.startPostProcessing) 
        
        
        # Setting right part layout
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.__start_b)
        
        
        ######  LEFT PART OF THE WIDGET  ######
        
        # Rover image
        fig=QPixmap(self.__dirtrs +'/img/postProcessing.png')  
        self.__icon=QLabel(self)
        self.__icon.setPixmap(fig)
        
        
        # Setting left part layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.__icon)
        

        
        ##### SETTING THE GLOBAL LAYOUT  ######
        
        rover_layout1 = QHBoxLayout()
        rover_layout1.addLayout(left_layout)
        rover_layout1.addLayout(right_layout)  

        self.setLayout(rover_layout1)
        
        
        #################  FUNCTIONS  #########################
        
        
    def openConfig(self):
        '''
        Opens the PostProcessingConfig subwindow
        '''
        try:
            print("a")
            subWindow = PostProcessingConfigWindow(self)
            subWindow.setModel(self.__postProcessing_model)
            subWindow.show()
        except Exception as e:
            print(e)
 

           
    def startPostProcessing(self):
        '''
        Launches the acquisition
        Notifies the Model
        Modifies the UI
        '''

            
        try:
            # modifying the UI
            self.__start_b.setDisabled(True)
            self.openConfig()
            info = InfoPostProcess()
            info.show()
            # Notifying the model
            real_postProcessing_model = self.__postProcessing_model.getInstancePostProcess()
            real_postProcessing_model.start()
            
            #Modifying the UI
            info.update() 
            info.show()
            info.update() 
            self.__start_b.setDisabled(False)
                
        except Exception as e:
            print(e)      

        
    