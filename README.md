# finance-utilities
Algoritmos de uso profissional para aplicações financeira direcionado a bolsa de valores nacional (B3 - IBOV)


1. Rodar B3.py para coletar os tickers da última atualização do índice IBOV
2. Colocar a lista no arquivo distortions.py >> carteira = [lista]
3. Rodar distortions.py e coletar sinais (quanto mais positivo mais forte o sinal de compra, quanto mais negativo, mais forte o sinal de venda)
4. (Bonus) Caso necessário, pode usar o main.py para transmitir os sinais via API e construir um dashboard visual
