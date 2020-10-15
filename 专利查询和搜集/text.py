from tkinter import *
import os
import cv2
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from contextlib import closing
import threading
# from pdf2image import convert_from_path
from PIL import Image, ImageEnhance,ImageTk
from tkinter.ttk import Treeview
import xlsxwriter
import xlrd
import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()
import fitz
import numpy as np
from io import BytesIO
from shutil import copyfile


demo = xlrd.open_workbook("./cleaned/demo.xlsx",on_demand=True)
sheet_names = demo.sheet_names()
final = xlsxwriter.Workbook("./cleaned/img.xlsx")
for sheet_name in sheet_names:
    worksheet = final.add_worksheet(sheet_name)
    nrows = demo.sheet_by_name(sheet_name).nrows
    ncols = demo.sheet_by_name(sheet_name).ncols
    i = 0
    cell_height = 140.0
    while i<nrows:
        worksheet.write_row(i,0,demo.sheet_by_name(sheet_name).row_values(i))
        if i >0:
            s = str(demo.sheet_by_name(sheet_name).cell(i,ncols-2)).replace("text:","").replace("'","")
            png = "png_get/"+s+".png"
            readIo = BytesIO()
            with open(png,mode='rb') as f:
                r = f.read()
                readIo.write(r)
            im= Image.open(readIo)
            original_width,original_height =im.size
            width = cell_height*original_width/original_height
            im.thumbnail((width,cell_height),Image.ANTIALIAS)
            im_bytes = BytesIO()
            worksheet.insert_image(i,ncols,png,{'image_data': im_bytes})
            tim = "png_time/"+s+".png"
            worksheet.insert_image(i,ncols+1,tim,{'x_scale': 0.3, 'y_scale': 0.3})
        i += 1
    worksheet.write(0,ncols,"专利图片")
    worksheet.write(0,ncols+1,"授权时间")
    worksheet.set_default_row(80)
    worksheet.set_row(0,25)
    worksheet.set_column(ncols-1,ncols,40)
    worksheet.set_column(ncols,ncols+1,25)
# final.close()