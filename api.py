from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/dados')
def get_dados():
    try:
        # Caminho ABSOLUTO do seu script (Windows)
        caminho_script = r"C:\Users\bmhil\Python\tradingview_scraper.py"
        
        # Executa o script (compatível com Windows)
        resultado = subprocess.check_output(
            ["python", caminho_script],
            shell=True,  # Necessário no Windows!
            text=True,
            stderr=subprocess.STDOUT
        )
        return resultado
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)