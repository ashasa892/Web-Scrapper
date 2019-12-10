import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

months = {'january':1, 'february':2, 'march':3,
          'april':4, 'may':5, 'june':6,
          'july':7, 'august':8, 'september':9,
          'october':10, 'november':11, 'december':12}
monthName = list(months.keys())
monthRep = ['0'+str(i+1) if i<9 else str(i+1) for i in range(12)]
requests.get("https://explosm.net/comics/5389/")

sMonth, sYear = input().split()
eMonth, eYear = input().split()
author = list(input().split())

loopRun = (int(eYear, 10) - int(sYear, 10))*12 + int(months[eMonth])- int (months[sMonth])
currMonth = int(months[sMonth])
currYear = int(sYear)

for i in range(loopRun):
    tempUrl = "https://explosm.net/comics/archive/"+str(currYear)+"/"+monthRep[currMonth-1]
    direc = str(currYear) + "/" + monthName[currMonth-1]
    try:
        os.makedirs(direc)
    except FileExistsError:
        pass
    
    for auth in author:
        url = tempUrl + "/" + auth.lower()
        
        try:
            response1 = requests.get(url)
            response1.raise_for_status()
            soup1 = BeautifulSoup(response1.content, 'html5lib')
            comics = soup1.find_all('div', 'archive-list-item')
            comicLinks = []
            
            for c in comics:
                tempLink = c.a['href']
                date = c.find('div', attrs = {'id':'comic-author'}).contents[0].strip()
                link = "https://explosm.net" + tempLink
                
                try:
                    response2 = requests.get(link)
                    response2.raise_for_status()
                    soup2 = BeautifulSoup(response2.content, 'html5lib')
                    comicDiv = soup2.find('div', attrs = {'id':'comic-wrap'})
                    linkToImage = comicDiv.img['src']
                    finalLinkToImage = "https:"+linkToImage
                    response3 = requests.get(finalLinkToImage)
                    downloadLoc = direc + "/"+date+"-" + auth +".png"
                    with open(downloadLoc, 'wb') as f:
                        f.write(response3.content)
                    print("Downloaded successfully to "+downloadLoc)
                    
                except HTTPError as http_err:
                    print("Cannot download {} comic for {} due to HTTP error: {}".format(auth, date, http_err))
                except Exception as err:
                    print("Cannot download {} comic for {} due to error: {}".format(auth, date, err))

                    
        except HTTPError as http_err:
            print("Cannot download {} comics for {}/{} due to HTTP error: {}".format(auth, currMonth, currYear, http_err))
        except Exception as err:
            print("Cannot download {} comics for {}/{} due to error: {}".format(auth, currMonth, currYear, error))
        
        pass
    currMonth += 1;
    if currMonth > 12:
        currMonth = 1
        currYear += 1
    pass

        

