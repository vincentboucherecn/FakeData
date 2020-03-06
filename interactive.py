__author__ = 'vincentboucher'
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import re
import random
from django.utils.encoding import smart_str
import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import Tk
import sys
root = Tk()
root.withdraw()

answer = simpledialog.askinteger("Input", "How many observation do you want in the Fake dataset?",
                                 minvalue=1000, maxvalue=1000000) # set number of observations. Must be large enough so that most factor values are generated with high probability
if (answer is None):
    sys.exit("Information is missing!")

n=int(answer)

filename =  filedialog.askopenfilename(initialdir = "./",title = "Select XML file",filetypes = (("xml files","*.xml"),("all files","*.*")))
if (filename is None):
    sys.exit("Information is missing!")
xmlfile = filename

publicdta = 0

result = tkinter.messagebox.askquestion("Public file", "Do you want to add a public micro-data file? (.csv files only)", icon='warning')
if result == 'yes':
    publicdta=1
    filename =  filedialog.askopenfilename(title = "Select CSV file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    if (filename is None):
        sys.exit("Information is missing!")
    pubfile = filename

if publicdta==1:
    dfpub = pd.read_csv(pubfile)
    dfpub.columns = map(str.lower, dfpub.columns)

filename = filedialog.asksaveasfile(title = "Name of the created .do file", mode='w', defaultextension=".do",filetypes = (("do files","*.do"),("all files","*.*")))
if (filename is None):
    sys.exit("Information is missing!")
dofile = filename.name

filename = filedialog.asksaveasfile(title = "Name of the created .csv file", mode='w', defaultextension=".csv",filetypes = (("csv files","*.csv"),("all files","*.*")))
if (filename is None):
    sys.exit("Information is missing!")
csvfile = filename.name

if (xmlfile is None) or ((publicdta ==1) and (pubfile is None)) or (dofile is None) or (csvfile is None):
    sys.exit("Information is missing!")

f= open(dofile,"w+") # *** change *** do-file to create labels

tree = ET.parse(xmlfile)
root = tree.getroot() # root of the tree (usually "codebook")

regex = r"\{(.*?)\}" # any stuff in brackets
matches = re.findall(regex, root[0].tag) # find stuff in bracket
namespace = "{" + matches[0] + "}" # character of the stuff in bracket

## the following lines remove the 'namespace' from variable names/id...
root[0].tag = root[0].tag.replace(namespace,'')
for elem in root.iter():
    elem.tag=elem.tag.replace(namespace, '')


# generates an empty dataset using variable ID
for vn in root.findall("./dataDscr/var"):
    cols = vn #.attrib["var"].split()
    df = pd.DataFrame(columns=cols)


# fill in the dataset and generate the do-file
for variables in root.findall("./dataDscr/var"):
    print(variables.attrib["name"])
    print(variables.attrib["ID"])
    df.rename(columns={variables.attrib["ID"]: variables.attrib["name"].lower()}, inplace=True)
    if (publicdta==1 and variables.attrib["name"].lower() in list(dfpub)):
        df[variables.attrib["name"].lower()]=[random.choice(dfpub[variables.attrib["name"].lower()]) for _ in range(n)]
    else:
        if variables.attrib["intrvl"]=='discrete':
            strlook1 = ".//*[@name='"+str(variables.attrib["name"])+"']/varFormat"
            for vtype in root.findall(strlook1):
                if vtype.attrib["type"]=='numeric':
                    lcat=[]
                    llab=[]
                    strlook = ".//*[@name='"+str(variables.attrib["name"])+"']/catgry/catValu"
                    cnt = 1
                    for cat in root.findall(strlook):
                        cnt = cnt + 1
                        lcat.append(cat.text.strip())
                    strlook = ".//*[@name='"+str(variables.attrib["name"])+"']/catgry/labl"
                    for cat in root.findall(strlook):
                        llab.append(cat.text.strip())
                    strt = "label define " + str(variables.attrib["name"].lower())
                    for pos in range(cnt-1):
                        strt = strt + " " + smart_str(lcat[pos]) + " `" + chr(34) + smart_str(llab[pos]) + chr(34) + chr(39)
                    f.write(smart_str(strt)+'\n')
                    strt = "label value " + str(variables.attrib["name"].lower()) + " " + str(variables.attrib["name"].lower())
                    f.write(smart_str(strt)+'\n')
                    df[variables.attrib["name"].lower()]=[random.choice(lcat) for _ in range(n)] # values are uniformly generated !! If someone had the frequencies, they could be included here
                else:
                    df[variables.attrib["name"].lower()]=[str(variables.attrib["name"].lower()) for _ in range(n)]

        elif variables.attrib["intrvl"]=='contin':
            df[variables.attrib["name"].lower()]=np.exp(np.random.normal(0,1,n)) # values are log-normally distributed !! If someone had the true distribution, change here.
    strlook = ".//*[@name='"+str(variables.attrib["name"])+"']/labl"
    for labels in root.findall(strlook):
        if (publicdta==1 and variables.attrib["name"].lower() in list(dfpub)):
            strin = "label variable " + str(variables.attrib["name"]) + " `" + chr(34) + "(pub)" + smart_str(labels.text.strip()) + chr(34) + chr(39)
        else:
            strin = "label variable " + str(variables.attrib["name"]) + " `" + chr(34) + smart_str(labels.text.strip()) + chr(34) + chr(39)
        
        f.write(smart_str(strin).lower()+'\n')

print(df.dtypes)
df.to_csv(csvfile) # saves the dataset as csv *** change *** for the wanted name

f.close()
