from bs4 import BeautifulSoup as bs
from os.path import exists as file_exists
import pandas as pd
import os
import time
import requests


def clear_function():
    os.system('cls' if os.name == 'nt' else 'clear')


def manufacture(text):
    global nameResult, valueResult

    nameStart = text.find(nameSub) + len(nameSub)
    nameEnd = text.find(tdSub)

    valueStart1 = text.find(valueSub) + len(valueSub)
    valueEnd1 = text.find(trSub)
    valueResult1 = text[valueStart1:valueEnd1]
    valueEnd2 = valueResult1.find('\n')
    valueResult2 = valueResult1[:valueEnd2]
    valueEnd3 = valueResult2.find(tdSub)

    valueResult = valueResult2[:valueEnd3]
    nameResult = var[nameStart:nameEnd]

    if any(c in 'amp;' for c in valueResult):
        valueResult = valueResult.replace('amp;', '')

    if any(c in 'amp;' for c in nameResult):
        nameResult = nameResult.replace('amp;', '')


def featuresTextEdit(text):
    global featuresText

    text = str(text)

    start = text.find('<ul>') + len('<ul>')
    end = text.find('</ul>')
    text = text[start:end]

    if text.find('</li>'):
        text = text.replace('</li>', '\n')
    if not text.find('<li>'):
        text = text.replace('<li>', '•')

    featuresText.append(text)


def fullPageEdit(text):
    global fullPage

    text = str(text)

    start = text.find('<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>')
    end = text.find('</style>') + len('</style>')

    delete = text[start:end]

    text = text.replace(delete, '')

    fullPage.append(text)


def getNameAndValue(text):
    global nameResult, valueResult

    nameStart = text.find(nameSub) + len(nameSub)
    nameEnd = text.find(tdSub)

    valueStart = text.find(valueSub) + len(valueSub)
    valueEnd = text.find(trSub)
    valueResult1 = text[valueStart:valueEnd]
    valueStart2 = valueResult1.find(spaceSub) + len(spaceSub)
    valueEnd2 = valueResult1.find(valueSub2)
    valueResult2 = valueResult1[valueStart2:valueEnd2]
    valueEnd3 = valueResult2.find(newlineSub)

    valueResult = valueResult2[:valueEnd3]
    nameResult = var[nameStart:nameEnd]

    if any(c in 'amp;' for c in valueResult):
        valueResult = valueResult.replace('amp;', '')

    if any(c in 'amp;' for c in nameResult):
        nameResult = nameResult.replace('amp;', '')


clear_function()

nameSub = '<td class="name">'
valueSub = '<td class="value">'
colspanNameSub = '<td colspan="2">'
tdSub = '</td>'
trSub = '</tr>'
spaceSub = '		'
newlineSub = '\n'
valueSub2 = '	</td'
nothing = ''
nameResult = ''
valueResult = ''

links = []
fullPage = []
fullPageAppend = []
names = []
html = []
className = []
productName = []
marketingText = []
marketingTextHtml = []
featuresText = []
featuresTextHtml = []
addFeaturesText = []
columns = {}
htmlEscapeTable = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}

filename = input("Enter file location(example: filename.xlsx): ")

clear_function()

while not file_exists(filename):
    print("File doesn't exist!")
    time.sleep(2)
    clear_function()
    filename = input("Enter file name(example: filename.xlsx): ")
    clear_function()

openfile = pd.read_excel(filename)
file = [openfile]

for i in openfile.index:
    links.append(openfile['httpDescriptionAlso'][i])

for i in range(0, len(links)):
    page = requests.get(links[i])

    pageContent = bs(page.content, 'html.parser')
    getHtml = bs(page.content, 'lxml')

    addHtml = [i for i in getHtml.find_all(class_=['mspec alt-0', 'mspec alt-0', 'alt-0', 'alt-1'])]

    className.append([i.text for i in pageContent.find_all(class_=['name', 'sectionHead'])])

    addNames = [i.text for i in pageContent.find_all(class_=['name', 'sectionHead'])]
    fullPageAppend.append(getHtml.find_all('html'))

    for productNameAppend in pageContent.find_all(class_='productName'):
        productName.append(productNameAppend.text)

    for marketingTextAppend in pageContent.find_all(class_='marketingText'):
        marketingText.append(marketingTextAppend.text)

    for addFeaturesTextAppend in pageContent.find_all(class_='featuresText'):
        addFeaturesText.append(addFeaturesTextAppend)

    for marketingTextHtmlAppend in pageContent.find_all(class_='marketingText'):
        marketingTextHtml.append(marketingTextHtmlAppend.text)

    for featuresTextHtmlAppend in pageContent.find_all(class_='featuresText'):
        featuresTextHtml.append(featuresTextHtmlAppend)

    for j in range(0, len(addNames)):
        if addNames[j] not in names:
            names.append(addNames[j])
        else:
            continue

    for j in range(0, len(addHtml)):
        html.append(addHtml[j])

    if '\xa0' in names:
        names.remove('\xa0')

    if ' ' in names:
        names.remove(' ')

    if 'Product Name' not in names:
        names.insert(0, 'Product Name')

    if 'Product Properties' in names:
        names.remove('Product Properties')

    addNames.clear()
    addHtml.clear()

    j = 0
    length = len(html)
    while j in range(0, length):
        if str(html[j]) == '<tr class="mspec sectionHead"><td colspan="2">Product Properties</td></tr>':
            del html[j]
            length = len(html)
        elif str(html[j]).find('<td class="image" rowspan="4">') > -1:
            del html[j]
            length = len(html)
        j += 1


for i in range(0, len(addFeaturesText)):
    featuresTextEdit(addFeaturesText[i])


for i in range(0, len(fullPageAppend)):
    fullPageEdit(fullPageAppend[i])


for i in range(0, len(names)):
    columns[names[i]] = [None]


for key, value in columns.items():
    value.remove(None)


for i in range(0, len(marketingTextHtml)):
    if "\'s" in str(marketingTextHtml[i]):
        marketingTextHtml[i] = str(marketingTextHtml[i]).replace("\'s", "'s")
    if '\xa0' in marketingTextHtml[i]:
        marketingTextHtml[i].replace('\xa0', '')
    if 'amp;' in marketingTextHtml[i]:
        marketingTextHtml[i].replace('amp;', '')


for i in range(0, len(featuresTextHtml)):
    if "\'s" in str(featuresTextHtml[i]):
        featuresTextHtml[i] = str(featuresTextHtml[i]).replace("\'s", "'s")
    if '\xa0' in featuresTextHtml[i]:
        featuresTextHtml[i].replace('\xa0', '')
    if 'amp;' in featuresTextHtml[i]:
        featuresTextHtml[i].replace('amp;', '')


for i in range(0, len(className)):
    if '\xa0' in className[i]:
        className[i].remove('\xa0')

    if ' ' in className[i]:
        className[i].remove(' ')

    if 'Product Properties' in className[i]:
        className[i].remove('Product Properties')


for i in range(0, len(html)):
    var = str(html[i])

    if 'Manufacturer' in var:
        manufacture(var)
    else:
        getNameAndValue(var)

    columns[nameResult].append(valueResult)


countMarket = 0
countFeatures = 0
columnsNotUsed = ['Product Name']
for i in range(0, len(className)):
    if 'NOT FOUND' in str(fullPage[i]) and 'No products found' in str(fullPage[i]):
        for key, value in columns.items():
            value.insert(i, '')
    else:
        for key, value in columns.items():
            if str(key) not in columnsNotUsed:
                if str(key) not in className[i]:
                    columns[key].insert(i, '')

    for j in range(0, len(productName)):
        for key, value in htmlEscapeTable.items():
            if str(key) in str(productName[j]):
                newName = ''.join(htmlEscapeTable.get(c, c) for c in str(productName[j]))
                if newName in str(fullPage[i]):
                    columns['Product Name'].append(productName[j])
        if str(productName[j]) in str(fullPage[i]):
            columns['Product Name'].append(productName[j])

    while countMarket < len(marketingText):
        if str(marketingText[countMarket]) in str(marketingTextHtml[i]):
            columns['Marketing Description'].append(marketingText[countMarket])
            countMarket += 1
            break

    while countFeatures < len(featuresText):
        amogus = str(featuresText[countFeatures])

        k = 0
        count = amogus.count('•')
        countMatches = 0
        while k < count:
            startCheck = amogus.find('•') + len('•')
            endCheck = amogus.find('\n')
            startDelete = amogus.find('•')
            endDelete = amogus.find('\n') + len('\n')

            textCheck = amogus[startCheck:endCheck]
            textDelete = amogus[startDelete:endDelete]

            if textCheck in str(featuresTextHtml[i]):
                countMatches += 1
            amogus = amogus.replace(textDelete, '')
            k += 1
        if countMatches == count:
            columns['Product Features'].append(featuresText[countFeatures])
            countFeatures+=1
            break


for key, value in columns.items():
    for i in range(0, len(value)):
        if "\r" in value[i]:
            value[i] = value[i].replace('\r', '')

for key, value in columns.items():
    print(key, ' : ', value)
    print(len(value))
    # if key == 'Marketing Description':
    #     for i in range(0, len(value)):
    #         print(value[i])
# for key, value in columns.items():
#     openfile.insert(loc=2, column=key, value=value)
# pd.DataFrame(openfile).to_excel(filename)

# for i in range(len(featuresTextHtml)):
#     print(i, ':', featuresTextHtml[i])
