from bs4 import BeautifulSoup
import requests
import pandas as pd

years = ['1930', '1934', '1938', '1950', '1954', '1958', '1962', '1966', '1970', '1974',
         '1978', '1982', '1986', '1990', '1994', '1998', '2002', '2006', '2010', '2014',
         '2018']

def get_matches(year):
    if year == '2022':
        web = 'https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup'
    else:
        web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(web)
    content = response.text

    soup = BeautifulSoup(content, 'lxml')

    matches = soup.find_all('div', class_='footballbox')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find('th', class_='fhome').get_text())
        score.append(match.find('th', class_='fscore').get_text())
        away.append(match.find('th', class_='faway').get_text())


    matches_dict = {'home': home, 'score': score, 'away': away}
    df_matches = pd.DataFrame(matches_dict)
    df_matches['year'] = year

    return df_matches

# HISTORICAL DATA
fifa = [get_matches(year) for year in years]
df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv('worldcup_historical_data.csv', index=False)

# FIXTURE 2022
df_fixture = get_matches('2022')
df_fixture.to_csv('worldcup2022_fixture.csv', index=False)