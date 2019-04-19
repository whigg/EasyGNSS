#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:15:03 2019

@author: edgar

This script was refractored from the work of Yusuke Takahashi, Taro Suzuki, Waseda University
See github : https://github.com/taroz/TouchRTKStation
    

"""

import sys
from PyQt5.QtWidgets import QApplication

from mainWidget import MainWidget

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    main = MainWidget()
    sys.exit(app.exec_())