from tkinter import *
from tkinter import messagebox
import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from contextlib import closing
import threading
from PIL import Image, ImageEnhance,ImageTk
from tkinter.ttk import Treeview
import xlsxwriter
import xlrd
import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()
import fitz
from shutil import copyfile
import threading
import webbrowser
import aiomultiprocess
import multiprocessing



class MyThread(threading.Thread):
    def __init__(self,func,*args):
        super().__init__()
        self.func = func
        self.args = args
        self.setDaemon(True)
        self.start()
    def run(self):
        self.func(*self.args)