# crypto_bot/bot.py
import ccxt
import time
import pandas as pd
from threading import Thread, Event
from cryptography.fernet import Fernet
import os
import json

# Encryption key management
def get_encryption_key():
    key_file = "secret.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    return key

def save_api_keys(api_key, api_secret, filename="api_keys.enc"):
    # If both keys are empty, delete the file if it exists
    if not api_key and not api_secret:
        if os.path.exists(filename):
            os.remove(filename)
        return
        
    # Otherwise encrypt and save the keys
    cipher = Fernet(get_encryption_key())
    data = {"api_key": api_key, "api_secret": api_secret}
    encrypted_data = cipher.encrypt(json.dumps(data).encode())
    with open(filename, "wb") as f:
        f.write(encrypted_data)

def load_api_keys(filename="api_keys.enc"):
    if not os.path.exists(filename):
        return None, None
    cipher = Fernet(get_encryption_key())
    with open(filename, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    data = json.loads(decrypted_data)
    return data["api_key"], data["api_secret"]

class TradingBot:
    def __init__(self, log_callback, api_key, api_secret, strategy='ma_crossover', 
                 buy_price=None, sell_price=None):
        self.running = Event()
        self.log_callback = log_callback
        self.exchange = ccxt.binanceus({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        self.strategy = strategy
        self.buy_price = float(buy_price) if buy_price else None
        self.sell_price = float(sell_price) if sell_price else None

    def get_position(self, symbol):
        try:
            balance = self.exchange.fetch_balance()
            return balance['total'].get(symbol.split('/')[0], 0)
        except Exception as e:
            self.log_callback(f"Error getting position: {e}", "ERROR")
            return 0

    def fetch_ohlcv(self, symbol, timeframe, limit):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_indicators(self, df, short_window, long_window):
        df['short_ma'] = df['close'].rolling(window=short_window).mean()
        df['long_ma'] = df['close'].rolling(window=long_window).mean()
        return df

    def trading_logic(self, df, symbol, amount):
        if self.strategy == 'price_targets':
            current_price = df.iloc[-1]['close']
            position = self.get_position(symbol)
            
            if position == 0:  # No position
                if self.buy_price and current_price <= self.buy_price:
                    self.log_callback(f"Buy price target reached: {current_price} <= {self.buy_price}", "INFO")
                    try:
                        order = self.exchange.create_market_buy_order(symbol, amount)
                        self.log_callback(f"Placed buy order: {order}", "SUCCESS")
                    except Exception as e:
                        self.log_callback(f"Error placing buy order: {e}", "ERROR")
            else:  # Have position
                if self.sell_price and current_price >= self.sell_price:
                    self.log_callback(f"Sell price target reached: {current_price} >= {self.sell_price}", "INFO")
                    try:
                        order = self.exchange.create_market_sell_order(symbol, position)
                        self.log_callback(f"Placed sell order: {order}", "SUCCESS")
                    except Exception as e:
                        self.log_callback(f"Error placing sell order: {e}", "ERROR")
        else:
            # Original MA crossover strategy
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            if previous['short_ma'] < previous['long_ma'] and latest['short_ma'] > latest['long_ma']:
                self.log_callback(f"Buy signal at {latest['close']}", "INFO")
                order = self.exchange.create_market_buy_order(symbol, amount)
                self.log_callback(f"Placed buy order: {order}", "SUCCESS")
            elif previous['short_ma'] > previous['long_ma'] and latest['short_ma'] < latest['long_ma']:
                self.log_callback(f"Sell signal at {latest['close']}", "INFO")
                order = self.exchange.create_market_sell_order(symbol, amount)
                self.log_callback(f"Placed sell order: {order}", "SUCCESS")

    def run(self, symbol, timeframe, short_window, long_window, amount):
        self.running.set()
        self.log_callback(f"Bot started for {symbol} with {self.strategy} strategy", "INFO")
        if self.strategy == 'price_targets':
            self.log_callback(f"Buy price target: {self.buy_price}, Sell price target: {self.sell_price}", "INFO")
        while self.running.is_set():
            try:
                df = self.fetch_ohlcv(symbol, timeframe, long_window + 1)
                df = self.calculate_indicators(df, short_window, long_window)
                self.trading_logic(df, symbol, amount)
                time.sleep(300)
            except Exception as e:
                self.log_callback(f"Error: {e}", "ERROR")
                time.sleep(60)
        self.log_callback("Bot stopped", "INFO")

    def stop(self):
        self.running.clear()