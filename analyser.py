from dataloader.coinbaseloader import CoinbaseLoader, Granularity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import mplfinance as mpf
import logging
from logging.handlers import RotatingFileHandler
import os
import yaml
import logging.config

def setup_logging(path='logger.yml', level=logging.DEBUG, env_key='LOG_CONFIG'):
    path = os.getenv(env_key, path)
    if (os.path.exists(path)):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)
    


    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, 'debug.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    
    logging.getLogger().addHandler(file_handler)

    


def main():
    loader = CoinbaseLoader()
    df_1 = loader.get_historical_data("eth-usdt", "2023-0101", "2023-06-30", Granularity.ONE_DAY)
    df_2 = loader.get_historical_data("btc-usdt", "2023-0101", "2023-06-30", Granularity.ONE_DAY)
    df_3 = loader.get_historical_data("sol-usdt", "2023-0101", "2023-06-30", Granularity.ONE_DAY)

    df_1['SMA20'] = df_1['close'].rolling(window=20).mean()
    df_1['SMA50'] = df_1['close'].rolling(window=50).mean()
    
    df_2['SMA20'] = df_2['close'].rolling(window=20).mean()
    df_2['SMA50'] = df_2['close'].rolling(window=50).mean()

    df_3['SMA20'] = df_3['close'].rolling(window=20).mean()  
    df_3['SMA50'] = df_3['close'].rolling(window=50).mean()  

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_figwidth(14)
    fig.set_figheight(7)

    ax1.plot(df_1.close, label='Ціна закриття')
    ax1.plot(df_1.SMA20, label='SMA 20 днів')
    ax1.plot(df_1.SMA50, label='SMA 50 днів')
    ax1.set_title('ETH-USDT')
    ax1.legend()
    ax1.grid()

    ax2.plot(df_2.close, label='Ціна закриття')
    ax2.plot(df_2.SMA20, label='SMA 20 днів')
    ax2.plot(df_2.SMA50, label='SMA 50 днів')
    ax2.set_title('BTC-USDT')
    ax2.legend()
    ax2.grid()

    ax3.plot(df_3.close, label='Ціна закриття')
    ax3.plot(df_3.SMA20, label='SMA 20 днів')
    ax3.plot(df_3.SMA50, label='SMA 50 днів')
    ax3.set_title('SOL-USDT')
    ax3.legend()
    ax3.grid()

    plt.show()

    # Об'єднання DataFrame за індексом
    df = pd.concat([df_1, df_2, df_3], axis=1)

    # Обробка та аналіз даних
    cm = df[['close', 'SMA20', 'SMA50']].corr()
    sns.heatmap(cm, annot=True)
    plt.show()

    df_1['LR'] = np.log(df_1.close/df_1.close.shift(1))
    plt.plot(df_1.LR)
    plt.grid()
    plt.show()

    print(f"volatility: {df_1.LR.std():0.4f}")

    df_2['LR'] = np.log(df_2.close/df_2.close.shift(1))
    plt.plot(df_2.LR)
    plt.grid()
    plt.show()

    df_3['LR'] = np.log(df_3.close/df_3.close.shift(1))
    plt.plot(df_3.LR)
    plt.grid()
    plt.show()

    # Обчислення RSA за 10, 20 та 50 днів
    df_1['RSA10'] = df_1['close'].pct_change(10).rolling(window=10).mean()
    df_1['RSA20'] = df_1['close'].pct_change(20).rolling(window=20).mean()
    df_1['RSA50'] = df_1['close'].pct_change(50).rolling(window=50).mean()

    df_2['RSA10'] = df_2['close'].pct_change(10).rolling(window=10).mean()
    df_2['RSA20'] = df_2['close'].pct_change(20).rolling(window=20).mean()
    df_2['RSA50'] = df_2['close'].pct_change(50).rolling(window=50).mean()

    df_3['RSA10'] = df_3['close'].pct_change(10).rolling(window=10).mean()
    df_3['RSA20'] = df_3['close'].pct_change(20).rolling(window=20).mean()
    df_3['RSA50'] = df_3['close'].pct_change(50).rolling(window=50).mean()

    # Побудова графіків RSA
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_figwidth(14)
    fig.set_figheight(7)

    ax1.plot(df_1['RSA10'], label='RSA 10 днів')
    ax1.plot(df_1['RSA20'], label='RSA 20 днів')
    ax1.plot(df_1['RSA50'], label='RSA 50 днів')
    ax1.set_title('ETH-USDT RSA')
    ax1.legend()
    ax1.grid()

    ax2.plot(df_2['RSA10'], label='RSA 10 днів')
    ax2.plot(df_2['RSA20'], label='RSA 20 днів')
    ax2.plot(df_2['RSA50'], label='RSA 50 днів')
    ax2.set_title('BTC-USDT RSA')
    ax2.legend()
    ax2.grid()

    ax3.plot(df_3['RSA10'], label='RSA 10 днів')
    ax3.plot(df_3['RSA20'], label='RSA 20 днів')
    ax3.plot(df_3['RSA50'], label='RSA 50 днів')
    ax3.set_title('SOL-USDT RSA')
    ax3.legend()
    ax3.grid()

    plt.show()

    #candle graph
    fig, axes = plt.subplots(1, 3, figsize=(14, 7))

    mpf.plot(df_1, type='candle', ax=axes[0], ylabel='Price') #For ETH
    mpf.plot(df_2, type='candle', ax=axes[1], ylabel='Price') #For BTC
    mpf.plot(df_3, type='candle', ax=axes[2], ylabel='Price') #For SOL
    
    plt.tight_layout()
    plt.show()

    print(f"volatility: {df_2.LR.std():0.4f}")


if __name__ == "__main__":
    setup_logging()
    main()
    
