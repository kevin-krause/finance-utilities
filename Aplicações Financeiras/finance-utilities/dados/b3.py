import bs4 as bs
import pickle
import requests


def save_ibov_tickers():
    B3_URL = 'http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraQuadrimestre.aspx?Indice=IBOV&idioma=pt-br'
    resp = requests.get(B3_URL)
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('tbody')

    tickers= []


    for row in table.findAll('tr',attrs={'disabled':""}):
        #print(row.text)
        ticker = row.findAll('td')[0].text.replace("\n","")
        tickers.append(ticker)

    print(tickers)

    return tickers

tickers = save_ibov_tickers()

#saves tickers in binary
with open("IBOVtickers.picke","wb") as file:
        pickle.dump(tickers,file)