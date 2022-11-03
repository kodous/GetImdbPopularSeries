import requests
from bs4 import BeautifulSoup

IMDB_URL = "https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv"

def sortIMDBRating(series):
    return series[1]['IMDB Rating']

def has_the_series_gone_up(html_obj):
    # gUP represent an object: if it is present it means that the TVSeries has gone up
    gUP = html_obj.find('span', attrs={'class': 'global-sprite titlemeter up'})
    return True

def was_the_series_in_the_first_100_past_week(current_position, positions_moved):
    return int(current_position) + int(positions_moved) < 100

def get_the_series_html_list(html_obj):
    return html_obj.find('tbody', attrs={'class': 'lister-list'}).find_all('tr')

def get_the_current_rank_and_the_velocity(html_obj):
    vel = html_obj.get_text().replace('\n', '').replace(')', '').split('(')
    return vel[0], vel[1]

# Send HTTPS request and create soup object
pageContent = requests.get(IMDB_URL).content
soup = BeautifulSoup(pageContent, 'html5lib')

# get the list of most 100 popular series
newSeries = []
seriesList = get_the_series_html_list(soup)
# loop thrpugh all popular series
for tr in seriesList:
    titleCol = tr.find('td', attrs={'class': 'titleColumn'})
    title = titleCol.a.get_text()
    velocity = titleCol.find('div', attrs={'class' : 'velocity'})
    if '(no change)' not in velocity:
        secInfo = velocity.find('span', attrs={'class': 'secondaryInfo'})
        try:
            has_the_series_gone_up(secInfo)
            current_rank, positions_moved = get_the_current_rank_and_the_velocity(velocity)
            if not was_the_series_in_the_first_100_past_week(current_rank, wapositions_movedyUP):
                rating = tr.find('td', attrs={'class':'ratingColumn imdbRating'}).find_all('strong')[0].get_text()
                newSeries.append((title, {'Current Rank':current_rank, 'Velocity': positions_moved, 'IMDB Rating': rating}))
        except:
            # we enter the exception only if the gUP object is null
            pass

newSeries.sort(key=sortIMDBRating, reverse=True)
for series in newSeries:
    print(series)
