#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:53:44 2019

@author: edgar

This script was originally made by Valentin in the previous ENSG-Géomatique project on low-cost GNSS 
"""

import virtual_keyboard
from PyQt5.QtWidgets import QLineEdit

class MyLineEdit(QLineEdit):
    '''
    MyLineEdit is the line editor tool of the application
    When the user wants to modify a string value in the configuration, MyLineEdit displays a virtual keyboard
    and save the modifications
    Inherits from QLineEdit
    
    Attributes:
        private VirtualKeyboard keyboard
        
    '''
    
    def __init__(self,*args, **kwargs):
        try:
            super(MyLineEdit, self).__init__(*args, **kwargs)
       
            self.__keyboard = virtual_keyboard.VirtualKeyboard()
            self.__keyboard.sigInputString.connect(self.updateTXT)

        except Exception as e:
            print(e)
            
                        
            
    ######  FUNCTIONS  ######
    
    
    
    def focusInEvent(self, event):
        '''
        Displays the virtual keyboard on screen
        '''
        self.parent().setFocus()
        self.__keyboard.raise_()
        self.__keyboard.show()
        super(MyLineEdit, self).focusInEvent(event)


    def updateTXT(self,text):
        '''
        Update text from keyboard entries
        '''
        self.setText(text)