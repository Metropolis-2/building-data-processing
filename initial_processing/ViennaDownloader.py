# -*- coding: utf-8 -*-
"""
Created on Wed May 19 13:08:22 2021

@author: andub
"""
import os
import sys
import zipfile
import requests

xmin = 78
xmax = 136

ymin = 62
ymax = 107

for x in range(xmin, xmax + 1):
    x_str = str(x)
    
    if x < 100:
        x_str = '0' + x_str
        
    for y in range(ymin, ymax + 1):
        y_str = str(y)
        
        if y < 100:
            y_str = '0' + y_str
            
        
        url = f'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/fmzk_bkm/{x_str}{y_str}_bkm.zip'
        filepath = f'data/vienna_LOD_0.4/{x_str}{y_str}_bkm.zip'
        
        try:
            r = requests.get(url)
            with open(filepath, 'wb') as f:
                f.write(r.content)
                
            # Check if file is valid. If file does not exist, then ret != None.    
            the_zip_file = zipfile.ZipFile(filepath)
            ret = the_zip_file.testzip()
                
            print(f'{x_str}{y_str}_bkm.zip exists. Downloaded.')
            
        except:
            print(f'{x_str}{y_str}_bkm.zip does not exist.')
            # Remove bogus file
            os.remove(filepath)
                    