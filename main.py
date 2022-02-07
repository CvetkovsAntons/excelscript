from bs4 import BeautifulSoup as bs
import os
import os.path as path
from os.path import exists as file_exists
import pandas as pd
import csv
import openpyxl
import os
import sys
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

openfile = pd.read_excel(filename)

row = 0
links = []
while row < len(openfile.index):
  # print(openfile.loc[row, 'httpDescriptionAlso'])
  page = requests.get(openfile.loc[row, 'httpDescriptionAlso'])
  links.append(page)
  pagecontent = bs(page.content, 'html.parser')
  names = [i.text for i in pagecontent.find_all(class_='name')]
  for i in range(0, len(names)-1):
    addcolumns = openfile.append(names[i], ignore_index=True)
    # addcolumns = pd.concat(file,names)
    addcolumns.to_excel(filename, index=False)
  row+=1

