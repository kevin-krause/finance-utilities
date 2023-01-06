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


@app.route('/distortions')
def pegardados():

    # Oganizando os dados (períodos mais curtos como intradiários - necessário mudar a API)
    end_d = datetime.now()
    start_d = end_d - timedelta(days=3)

    carteira = ['VALE3.SA', 'VIVT3.SA', 'WEGE3.SA', 'YDUQ3.SA']

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
                         & (rsi >= sell_force), -1, trend)
        return trend

    ind = vbt.IndicatorFactory(
        class_name='distortions',
        short_name='distortions',  # Apelido
        input_names=['close'],  # Dados que vão passar pela função
        param_names=['maf_window', 'mas_window', 'rsi_window',
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
    dadoAPI = pd.DataFrame(res.value) 
    dadoAPI = res.value.to_list()
    print (dadoAPI)

    # print(res.value.to_string())

