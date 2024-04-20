import os
import re
import sys
import time
import shutil
import requests
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def main():
    urlFile = open('UrlsList.txt','r', encoding='utf-8-sig')
    urls = urlFile.readlines()

    urls = [url.strip() for url in urls]
    imgToDelete=""

    for url in urls:
        url=str(url)
        serie = url.split("/")[4]
        comicType = url.split("/")[5].split("?")[0]
        imgFolder = serie+"_img" 
        
        if "Issue" in comicType:
            cbrFileName = serie.replace("-"," ") + " - " + comicType.replace("-"," ") +".cbr"
            deleteImgFolder(imgFolder)
        
        elif "Part" in comicType:
            cbrFileName = serie.replace("-"," ") + " - " + comicType.replace("-"," ")[1] + ".cbr"
            if "Part-1" in url:
                deleteImgFolder(imgFolder)

        else:
            cbrFileName = serie.replace("-"," ") + ".cbr"
            deleteImgFolder(imgFolder)
        
        downloadComics(url, serie, cbrFileName, imgFolder)
        imgToDelete = imgFolder

    deleteImgFolder(imgFolder)

def deleteImgFolder(imgFolder):
    if os.path.exists(imgFolder) and os.path.isdir(imgFolder):
        shutil.rmtree(imgFolder)

def downloadComics(url, serie, cbrFilename, imgFolder):
    url = url + "&s=&readType=1&quality=hq"
    imgLinks = "imgLinks.txt"
    htmlSource = "htmlSource.txt"
    cbrPath = serie +"\\"  + cbrFilename

    downloadSource(url, htmlSource)
    extractLink(htmlSource, imgLinks)
    downloadImg(imgLinks, imgFolder)
    buildCbr(imgFolder, cbrPath)

def downloadSource(url, htmlSource):
    chromedriverPath = 'C:\\Program Files\\chromedriver-win64\\chromedriver.exe'
    service = Service(executable_path=chromedriverPath)  
    
    chromedriver = webdriver.Chrome(service=service)   
    print("URL being loaded:", url)
    print(type(url))
    chromedriver.get(url)

    
    time.sleep(3)

    source = chromedriver.page_source
    with open(htmlSource, 'w', encoding='utf-8') as fichier:
        fichier.write(source)
    
    chromedriver.quit

def extractLink(htmlSource, imgLinks):
    with open(htmlSource, 'r', encoding='utf-8') as file:
        content = file.read()

    startIdx = content.find('<div id="divImage"')
    endIdx = content.find('</div>', startIdx)
    
    if startIdx != -1 and endIdx != -1:
        length = endIdx - startIdx + 6
        extractedContent = content[startIdx:startIdx + length]
        
        with open(htmlSource, 'w', encoding='utf-8') as file:
            file.write(extractedContent)
            links = re.findall(r'<img[^>]*\ssrc="([^"]+)"', extractedContent)
            
            with open(imgLinks, 'w', encoding='utf-8') as file:
                for link in links:
                    file.write(link + '\n')

def downloadImg(imgLinks, imgFolder):
    if not os.path.exists(imgFolder):
        os.makedirs(imgFolder)
    
    with open(imgLinks, 'r') as file:
        links = [line.strip() for line in file if line.strip()]

    for idx, link in enumerate(links, start=1):
        try:
            response = requests.get(link)
            response.raise_for_status()

            img_filename = f"{idx:03}.jpg"
            path_to_save = os.path.join(imgFolder, img_filename)

            with open(path_to_save, 'wb') as img_file:
                img_file.write(response.content)
            print(f"Downloaded {img_filename} from {link}")

        except requests.RequestException as e:
            print(f"Failed to download {link}: {e}") 

def buildCbr(imgFolder, cbrPath):
    if os.path.isfile(cbrPath):
        os.remove(cbrPath)

    shutil.make_archive(cbrPath, 'zip', imgFolder)
    os.rename(f"{cbrPath}.zip", cbrPath)

main()
