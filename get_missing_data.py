from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd


years = ['1930', '1934', '1938', '1950', '1954', '1958', '1962', '1966', '1970', '1974',
         '1978', '1982', '1986', '1990', '1994', '1998', '2002', '2006', '2010', '2014',
         '2018']


path = '/Users/alberespi/Documents/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

def get_missing_data(year):
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    driver.get(web)

    matches = driver.find_elements(by='xpath', value='//tr[@style="font-size:90%"]')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find_element(by='xpath', value='./td[1]').text)
        score.append(match.find_element(by='xpath', value='./td[2]').text)
        away.append(match.find_element(by='xpath', value='./td[3]').text)

    dict_matches = {'home': home, 'score': score, 'away': away}
    df_matches = pd.DataFrame(dict_matches)
    df_matches['year'] = year
    time.sleep(2)

    return df_matches

fifa_wc = [get_missing_data(year) for year in years]
driver.quit()

df_worldcups = pd.concat(fifa_wc, ignore_index=True)
df_worldcups.to_csv('worldcup_historical_missing_data.csv', index=False)