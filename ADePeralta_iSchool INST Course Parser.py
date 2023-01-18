#URL to use for this question:
#   https://academiccatalog.umd.edu/undergraduate/approved-courses/inst/

import urllib.request, urllib.parse, urllib.error
import re
import ssl
#____FUNCTIONS_____
#takes URL,
#returns the list of the rows of the course block
#(<div class="courseblock">)
def getHTML(url):
    #search for link values within URL input
    #ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    html = urllib.request.urlopen(url, context=ctx).read()

    fullPage = str(html).split('<div class="courseblock">')

    cbList = []
    for line in fullPage:
        if '<p class="courseblocktitle noindent">' in line:
            begin = line.find(">", 50)+1
            end = line.find("<", begin)
            cbRows = line[begin:end]

            cbList.append(cbRows)
    
    return cbList

#takes list of rows of the rows of the course block,
#returns dict of course codes, titles and credits
def makeCourseDict(cbList):
    courseDict = {}

    for item in cbList:
        if "INST" in item:
            #Finds course code
            begin = item.find("I")
            end = item.find(" ", begin)
            code = item[begin:end]


            #Finds course title
            start = item.find(" ")+1
            stop = item.find ("(", start)
            title = item[start:stop]

        
            #Finds course credit
            first = item.find("(")+1
            last = item.find(")", first)
            credit = item[first:last]
        

            courseDict[code]=[title, credit]
 
    return courseDict

#takes dictionary of courses,
#returns list of courses at given level
def atLevel(level, courseDict):
    levelDict = {}
    num = int(level) #Changes level from str to int 
    courseCode = '' 
    courseTC = '' #Course title and credit 
    
    'Level 400 classes'
    if num >= 400:
        for i in courseDict: #Iterates through each item in courseDict 
            if int(i[4]) == 4: #If item has a 4 in the fourth index 
                courseCode = i 
                courseTC = courseDict[i]
                #Creates dictionary with courseCode as the key and courseTC as value
                levelDict[courseCode] = courseTC 
                
    elif num < 400 and num >= 300:
        for i in courseDict:
            if int(i[4]) == 3: #If item has a 3 in the fourth index 
                courseCode = i
                courseTC = courseDict[i]
                levelDict[courseCode] = courseTC
                
    elif num < 300 and num >= 200:
        for i in courseDict:
            if int(i[4]) == 2: #If item has a 2 in the fourth index 
                courseCode = i
                courseTC = courseDict[i]
                levelDict[courseCode] = courseTC
                
    elif num <=200:
        for i in courseDict:
            if int(i[4]) == 1: #If item has a 1 in the fourth index 
                courseCode = i
                courseTC = courseDict[i]
                levelDict[courseCode] = courseTC

    return levelDict

#MAIN FUNCTION 
website = input("Enter URL - ")
level = input("Enter level (100, 200, 300, or 400) - ")

courseBlock = getHTML(website)
courseDct = makeCourseDict(courseBlock)
levelDct = atLevel(level, courseDct)

print(levelDct)        
