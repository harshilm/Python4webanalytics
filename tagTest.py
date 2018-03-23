"""
@author: absharm
"""
#all imports
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from time import sleep
import requests, bs4

#global variables
HTML_string = '''<!DOCTYPE html>
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>

<h2>Tag Table</h2>

<table>
<tr>
    <th>Page URL</th>
    <th>Page Name</th>
    <th>Events</th>
  </tr>'''
  
target_url = 'http://www.url .com' #starting url

# findalllinks.py - find all the links on the page
def findalllinks (url):

    #download the page
    print ('parsing...') #displaying text while parsing the page
    res = requests.get(url) #takes the string of the url to download
    res.raise_for_status() #will raise an exception if there is error downloading
    
    #retrieve all the links
    abhiSoup = bs4.BeautifulSoup(res.text)
    linkel = abhiSoup.select('body a') #could be targeted to links within any element on page 
    
    #return a set of links
    numOpen = len(linkel)
    #print (numOpen) #optional for console validation
    linkel2 =[]  
    for i in range(numOpen):
        linkel2 = linkel2 + [(linkel[i].get('href'))]
    return linkel2 

# Visit the page
def pagehits(url):
    global HTML_string
    #visit the page in a headless version of firefox
    options = Options()
    options.add_argument("--headless")
    #starting selenium controlled web browser
    #latest geckodriver is needed to run firefox with selenium
    browser = webdriver.Firefox(firefox_options=options, executable_path="C:\\Users\\dirLocation\\geckodriver.exe")
    browser.get(url)
    #give page time to load
    sleep(1)
    #log events and pagename
    #put the block in try/except
    try:
        pageName = browser.execute_script("return (s.pageName);")
        events = browser.execute_script("return (s.events);")
        print(pageName) #optional for console validation
        print(events) #optional for console validation
        HTML_string += '''<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>'''.format(url,pageName,events)
        HTML_string +=	"</tr>"
        
        
    except WebDriverException:
        print("Exception on {}".format(url))
    browser.quit()

url_list = findalllinks(target_url)
# Iterate the links and collect data
for i in range(len(url_list)):
#for i in range(10,15):
    tag_link = str(url_list[i])
    if tag_link.startswith('/'):
        pagehits(target_url+tag_link)
    elif tag_link.startswith('http' or 'www'):
        pagehits(tag_link)
    else:
        continue
        
#Append the closing html
HTML_string += '''</table></body></html>'''
# Write the HTML to a file
HTML_file= open("file.html","w")
HTML_file.write(HTML_string)
HTML_file.close()
