from tradingview_ta import TA_Handler, Interval
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

# Função para pegar todos os tickers da B3 do Fundamentus
def get_all_b3_tickers():
    print("Obtendo lista de tickers...")
    url = "https://www.fundamentus.com.br/resultado.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find("table", {"id": "resultado"})
        return [row.find('a').text.strip() for row in tabela.find_all("tr")[1:]]
    except Exception as e:
        print(f"Erro ao buscar tickers: {e}")
        return []

# Função principal para análise de cada ticker
def analyze_ticker(ticker):
    try:
        analysis = TA_Handler(
            symbol=ticker,
            screener="brazil",
            exchange="BMFBOVESPA",  # Nome oficial no TradingView
            interval=Interval.INTERVAL_1_DAY
        )
        data = analysis.get_analysis()
        
        return {
            "Ticker": ticker,
            "Preço": data.indicators["close"],
            "Recomendação": data.summary["RECOMMENDATION"],
            "RSI": data.indicators.get("RSI", "N/A"),
            "MACD": data.indicators.get("MACD.macd", "N/A"),
            "Volume": data.indicators["volume"],
            "Variação %": data.indicators["change"]
        }
    
    except Exception as e:
        print(f"Erro no ticker {ticker}: {str(e)}")
        return None

# Configurações
all_tickers = get_all_b3_tickers()
max_workers = 5  # Reduza se tiver problemas
delay = 1  # Segundos entre requests

# Processamento paralelo
results = []
print(f"Iniciando análise de {len(all_tickers)} ativos...")

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    for i, result in enumerate(executor.map(analyze_ticker, all_tickers)):
        if result:
            results.append(result)
        if (i + 1) % 10 == 0:
            print(f"Progresso: {i + 1}/{len(all_tickers)}")
            time.sleep(delay)

# Salvar resultados
pd.set_option('display.max_rows',None)
df = pd.DataFrame(results)
df.to_csv("analise_completa_b3.csv", index=False)
print("Análise salva em analise_completa_b3.csv!")
print(df)