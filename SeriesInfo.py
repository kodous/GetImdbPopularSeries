import requests
from bs4 import BeautifulSoup

def sortIMDBRating(series):
    return series[1]['IMDB Rating']


# Send HTTPS request and create soup object
imdbURL = "https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv"
pageContent = requests.get(imdbURL).content
soup = BeautifulSoup(pageContent, 'html5lib')

# get the list of most 100 popular series
newSeries = []
seriesList = soup.find('tbody', attrs={'class': 'lister-list'}).find_all('tr')
# loop thrpugh all popular series
for tr in seriesList:
    titleCol = tr.find('td', attrs={'class': 'titleColumn'})
    title = titleCol.a.get_text()
    velocity = titleCol.find('div', attrs={'class' : 'velocity'})
    if '(no change)' not in velocity:
        secInfo = velocity.find('span', attrs={'class': 'secondaryInfo'})
        try:
            # gUP represent an object: if it is present it means that the TVSeries has gone up
            gUP = secInfo.find('span', attrs={'class': 'global-sprite titlemeter up'})
            vel = velocity.get_text().replace('\n', '').replace(')', '').split('(')
            c_rank = vel[0]
            wayUP = vel[1]
            # if it is > 100, it means that this series was not on the list the past week
            if(int(c_rank) + int(wayUP)) >= 100:
                rating = tr.find('td', attrs={'class':'ratingColumn imdbRating'}).find_all('strong')[0].get_text()
                newSeries.append((title, {'Current Rank':c_rank, 'Velocity': wayUP, 'IMDB Rating': rating}))
        except:
            # we enter the exception only if the gUP object is null
            pass

newSeries.sort(key=sortIMDBRating, reverse=True)
for series in newSeries:
    print(series)
