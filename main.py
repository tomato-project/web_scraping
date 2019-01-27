import requests
import pandas as pd
from bs4 import BeautifulSoup

website = 'http://greenbondplatform.env.go.jp/greenbond/list/'
r = requests.get(website)
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('tr')
#<table class="first"> <tbody> <tr> <th> <a> </a> </th> </tr> </tbody> </table>

def create_dataframe(results,keyword):
    table = []
    for a in results:
        x = a.find_all([keyword])
        row = [a.text for a in x]
        table.append(row)
    return table

issuer = pd.DataFrame(create_dataframe(results,'th'), columns=["発行体","発行時期", "発行金額","資金使途","利率","償還期間"]).loc[:,['発行体']]
table = pd.DataFrame(create_dataframe(results,'td'), columns=["発行時期", "発行金額","資金使途","利率","償還期間"])

result = pd.concat([issuer, table], axis=1, sort=False)
clean_df = result[~result["発行体"].isin(["発行体"])]

clean_df.to_csv('masterfile.csv', encoding="Shift-JIS")

print('Done. check the output csv ("masterfile.csv")')
