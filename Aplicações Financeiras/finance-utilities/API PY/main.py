from flask import Flask, jsonify
import json
import pandas as pd

app = Flask(__name__)

# Cosntruir as funcionalidades
@app.route('/')
def pegardados():
  dadosAPI = pd.read_csv('./file_path.csv')
  dadosAPI = (dadosAPI.to_string())
   

  resposta= {'dados': dadosAPI.get()}

  return jsonify(resposta)

 

app.run()

