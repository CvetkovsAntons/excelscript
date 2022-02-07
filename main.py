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
file = [openfile]

links = []
names = []
groups = []
for i in openfile.index:
  links.append(openfile['httpDescriptionAlso'][i])

for i in range(0, len(links)):
  page = requests.get(links[i])
  pagecontent = bs(page.content, 'html.parser')
  addnames = [i.text for i in pagecontent.find_all(class_='name')]
  addgroups = [i.text for i in pagecontent.find_all(class_=['mspec alt-0', 'mspec alt-1'])]
  for i in range(0, len(addnames)):
    if addnames[i] not in names:
      names.append(addnames[i])
    else:
      continue
  for i in range(0, len(addgroups)):
    if addgroups[i] not in groups:
      groups.append(addgroups[i])
    else:
      continue
  addnames.clear()
  addgroups.clear()

del names[0]

for i in range(0, len(names)):
  for j in range(0, len(groups)):
    if pagecontent.find_all(class_=['mspec alt-0', 'mspec alt-1'])
      openfile.insert(loc=i+2, column=names[i], value=names[i])
  pd.DataFrame(openfile).to_excel(filename)

