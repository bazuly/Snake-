import requests
import json
import pandas as pd


link = 'https://api.opendota.com/api/heroStats'

r = requests.get(link)

data = json.loads(r.text)

df = pd.DataFrame(data)

df.head(10)

df.to_csv('data_1.csv', sep=';', encoding='utf-8')


