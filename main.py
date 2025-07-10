import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calcular_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generar_grafico(ticker):
    print(f"\nDescargando datos para: {ticker}")

    data = yf.Ticker(ticker).history(
        start="2023-01-01",
        end="2023-07-01",
        auto_adjust=True
    )

    if data.empty:
        print(f"No se descargaron datos para {ticker}")
        return

    # Media móvil de 20 días para BB
    data['MA20'] = data['Close'].rolling(window=20).mean()
    std20 = data['Close'].rolling(window=20).std()
    data['BB_up'] = data['MA20'] + 2 * std20
    data['BB_down'] = data['MA20'] - 2 * std20

    # RSI 14 días
    data['RSI'] = calcular_rsi(data)

    # Gráfico principal: Precio y Bandas de Bollinger
    plt.figure(figsize=(12, 8))

    plt.subplot(2,1,1)
    plt.plot(data.index, data['Close'], label='Precio Ajustado')
    plt.plot(data.index, data['MA20'], label='MA 20 días', color='orange')
    plt.plot(data.index, data['BB_up'], label='Banda Superior', color='green')
    plt.plot(data.index, data['BB_down'], label='Banda Inferior', color='red')
    plt.title(f'{ticker} - Precio con Bandas de Bollinger')
    plt.xlabel('Fecha')
    plt.ylabel('Precio (USD)')
    plt.legend()
    plt.grid(True)

    # Gráfico RSI
    plt.subplot(2,1,2)
    plt.plot(data.index, data['RSI'], label='RSI 14 días', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Sobrecompra (70)')
    plt.axhline(30, color='green', linestyle='--', label='Sobreventa (30)')
    plt.title(f'{ticker} - RSI')
    plt.xlabel('Fecha')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    filename = f"grafico_{ticker}_bb_rsi.png"
    plt.savefig(filename, dpi=300)
    print(f"Gráfico con BB y RSI guardado como '{filename}'")

    plt.show()

def main():
    tickers = ["AAPL", "MSFT", "TSLA"]
    for ticker in tickers:
        generar_grafico(ticker)

if __name__ == "__main__":
    main()
