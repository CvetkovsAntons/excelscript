from bs4 import BeautifulSoup as bs
import os
import os.path as path
from os.path import exists as file_exists
import pandas as pd
import csv
import openpyxl
import time
import requests
import random

def clear_function() :
  os.system('cls' if os.name == 'nt' else 'clear')

clear_function()

filename = input("Enter file location(example: filename.xlsx): ")
clear_function()
while file_exists(filename) == False:
    print("File doesn't exist!")
    time.sleep(2)
    clear_function()
    filename = input("Enter file name(example: filename.xlsx): ")
    clear_function()



openfile = pd.read_excel(filename, usecols='B')
row = 0
links = []
while row < len(openfile.index):
  # print(openfile.loc[row, 'httpDescriptionAlso'])
  page = requests.get(openfile.loc[row, 'httpDescriptionAlso'])
  links.append(page)
  pagecontent = bs(page.content, 'html.parser')
  print(pagecontent)
  row+=1

