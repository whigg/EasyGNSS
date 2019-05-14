#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:15:03 2019

@author: edgar

This script was refractored from the work of Yusuke Takahashi, Taro Suzuki, Waseda University
See github : https://github.com/taroz/TouchRTKStation

It is the work of ENSG-Geomatique students on the demand of Mr Jean-Yves Perrin and Mr Francklin N'Guyen who where
the initiators of a previous low-cost GNSS software in C, RTKBase
See github : https://github.com/Francklin2/RTKLIB_Touchscreen_GUI

The student team was composed of Nassim, Sanam, Arthur and Edgar

This is an open source project and we highly recommand people to make further developpments 

"""

import sys
from PyQt5.QtWidgets import QApplication

from mainWidget import MainWidget

if __name__ == '__main__':
    
    '''
    main.py is the entry point of the application
    '''
    
    app = QApplication(sys.argv)
    main = MainWidget()
    sys.exit(app.exec_())