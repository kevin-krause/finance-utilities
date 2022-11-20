from flask import Flask, jsonify
import json
import pandas as pd
import vectorbt as vbt
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import pandas as pd
import numpy as np

app = Flask(__name__)

# Cosntruir as funcionalidades
@app.route('/d')
def pegardados():

  # Oganizando os dados (períodos mais curtos como intradiários - necessário mudar a API)
  end_d = datetime.now()
  start_d = end_d - timedelta(days=3)

  '''  carteira = ['ABEV3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBDC4.SA', 'BBSE3.SA', 'BEEF3.SA', 'BPAC11.SA', 'BRAP4.SA', 'BRFS3.SA', 'BRKM5.SA', 'BRML3.SA', 'CCRO3.SA', 'CIEL3.SA', 'CMIG4.SA', 'COGN3.SA', 'CPFE3.SA', 'CPLE6.SA', 'CRFB3.SA', 'CSAN3.SA', 'CSNA3.SA', 'CVCB3.SA', 'CYRE3.SA', 'ECOR3.SA', 'EGIE3.SA', 'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENBR3.SA', 'ENEV3.SA', 'ENGI11.SA', 'EQTL3.SA', 'EZTC3.SA', 'FLRY3.SA', 'GGBR4.SA','GOAU4.SA', 'GOLL4.SA', 'HAPV3.SA', 'HYPE3.SA', 'IRBR3.SA', 'ITSA4.SA', 'ITUB4.SA', 'JBSS3.SA', 'JHSF3.SA', 'KLBN11.SA', 'LREN3.SA', 'MGLU3.SA', 'MRFG3.SA', 'MRVE3.SA', 'MULT3.SA', 'NTCO3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA', 'PRIO3.SA', 'QUAL3.SA', 'RADL3.SA', 'RAIL3.SA', 'RENT3.SA', 'SANB11.SA', 'SBSP3.SA', 'SULA11.SA', 'SUZB3.SA', 'TAEE11.SA', 'TIMS3.SA', 'TOTS3.SA', 'UGPA3.SA', 'USIM5.SA', 'VALE3.SA', 'VIVT3.SA', 'WEGE3.SA', 'YDUQ3.SA']'''

  carteira = ["VALE3.SA"]

  mdata = pd.DataFrame()
  for t in carteira:
      mdata[t] = yf.download(t, start=start_d, end=end_d,
                            interval='1d')['Adj Close']

  def distortions(close, maf_window=3, mas_window=5, rsi_window=14, buy_force=30, sell_force=70):

     
      # 1 Crossed MA (Supper Trend)
      ma_fast = vbt.MA.run(close, window=maf_window)  # Configurando MA
      ma_slow1 = vbt.MA.run(close, window=mas_window)  # Configurando MA

      # 2 RSI (Índice de Força Relativa)
      # Configurando RSI
      rsi = vbt.RSI.run(close, window=rsi_window).rsi.to_numpy()

      # 3 Breakout
      '''high_p = close
    high_m = close[media_close:].mean()'''

      # Filtro
      trend = np.where((ma_fast.ma_crossed_above(ma_slow1))
                      & (rsi <= buy_force), 1, 0)
      trend = np.where((ma_fast.ma_crossed_below(ma_slow1))
                      & (rsi >= 3), -1, trend)
      return trend


  ind = vbt.IndicatorFactory(
      class_name='distortions',
      short_name='distortions',  # Apelido
      input_names=['close'],  # Dados que vão passar pela função
      param_names=['maf_window', 'mas_window', 'rsi_window' ,
                  'buy_force', 'sell_force'],  # Nome dos parâmetros passados
      output_names=['value']
  ).from_apply_func(
      distortions,
      maf_window=3,
      mas_window=5,
      rsi_window=14,
      buy_force=30,
      sell_force=70  # Configure as janelas
  )

  # print(pandasData)

  res = ind.run(
      mdata,
  )


  # CSV
  dadoAPI = res.value
  # print(dadoAPI) = dadoAPI.to_json() 
  #print(dadoAPI)

  return (dadoAPI)

 

# Rodar API
app.run()

# tabela = pd.read_csv('2022/py/Simple-TF/Heatmap/dados/dados.csv')

