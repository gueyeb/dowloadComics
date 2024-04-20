# DownloadComics

## Prerequisites
- python 3.12.3
- pip 24.0
- libraries: requests, selenium `pip install requests selenium`
- chromedriver:  find here: https://googlechromelabs.github.io/chrome-for-testing/
- update your chromedriver path in buildCBR: line 61

## Notes
Every path are relatives, you may want to run the scripts from a folder

## extractIssuesFromSummary
`py extractIssuesFromSummary.py https://readcomiconline.li/Comic/.../`
Extract all issues link from a summary page in a file **UrlsList.txt**  
(summary page example: https://readcomiconline.li/Comic/Ultimate-Spider-Man-2024) 


## BuildCBR
`py buildCBR.py`
Download images and build CBR from the URLs in **UrlsList.txt**
