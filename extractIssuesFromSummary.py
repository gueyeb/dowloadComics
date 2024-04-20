import requests
import sys
import re
import os

def save_html(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
    
    except requests.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier : {e}")

def extractIssue(htmlSource, imgLinks, startStr, endStr, regex):
    with open(htmlSource, 'r', encoding='utf-8') as file:
        content = file.read()

    startIdx = content.find(startStr)
    endIdx = content.find(endStr, startIdx)
    
    if startIdx != -1 and endIdx != -1:
        length = endIdx - startIdx
        extractedContent = content[startIdx:startIdx + length]
        
        with open(htmlSource, 'w', encoding='utf-8') as file:
            file.write(extractedContent)
            links = re.findall(regex, extractedContent)
            with open(imgLinks, 'w', encoding='utf-8') as file:
                for link in links:
                    file.write('https://readcomiconline.li'+link + '\n')

def revertLines(filename):
    with open(filename, 'r', encoding='utf-8') as fichier:
        line = fichier.readlines()
    reversedLine = line[::-1]
    with open(filename, 'w', encoding='utf-8') as fichier:
        fichier.writelines(reversedLine)



url = sys.argv[1]
filename = 'summary.txt'
save_html(url, filename)
extractIssue(filename, 'UrlsList.txt','<ul class="list">', '</ul>', r'href="([^"]*)"' )
revertLines('UrlsList.txt')

if os.path.isfile(filename):
        os.remove(filename)
