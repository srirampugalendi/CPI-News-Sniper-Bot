import sys
import ccxt
import time
import threading
import configparser

'''
This application opens a long and a short position at a specified epoch time.
Set Capital, Leverage, Symbol and Epoch time (time of CPI news release in GMT) details in the config file.
'''


def excecute_long_and_short():
    if debug:
        print("\nDebug mode enabled. Real orders will not be executed.")
    else:
        print("\nFunction executed at:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        # Place a long order
        place_order(symbol, 'buy', quantity, 'LONG')
        print()
        # Place a short order
        place_order(symbol, 'sell', quantity, 'SHORT')


def run_at_epoch(epoch_time, func):
    # Calculate the delay in seconds
    current_time = time.time()
    delay = epoch_time - current_time

    # Ensure the delay is not negative
    if delay < 0:
        print("Specified epoch time is in the past. Exiting.")
        return

    # Function to update and display the time remaining
    def update_remaining_time():
        while True:
            current_time = time.time()
            remaining_time = epoch_time - current_time
            if remaining_time <= 0:
                break
            # Print the remaining time, overwriting the previous line
            sys.stdout.write(f"\rTime remaining: {remaining_time:.2f} seconds")
            sys.stdout.flush()
            time.sleep(0.1)
        # print("\nTime is up!")

    # Start the timer thread
    timer = threading.Timer(delay, func)
    timer.start()

    # Update the remaining time in the main thread
    update_remaining_time()


# Function to set leverage for a symbol
def set_leverage(symbol, leverage):
    try:
        binance.fapiPrivate_post_leverage({
            'symbol': symbol,
            'leverage': leverage,
        })
        print(f"Leverage set to {leverage}x for {symbol}")
    except Exception as e:
        print(f"An error occurred while setting leverage: {str(e)}")


# Function to get symbol precision
def get_symbol_precision(symbol):
    market = binance.market(symbol)
    return market['precision']['amount']


# Function to place a market order
def place_order(symbol, side, quantity, position_side):
    try:
        order = binance.create_order(
            symbol=symbol,
            type='market',
            side=side,
            amount=quantity,
            params={'positionSide': position_side}  # Specify position side for hedge mode
        )
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"An error occurred while placing the order: {str(e)}")


def check_usdc_balance():
    try:
        balance = binance.fetch_balance({'type': 'future'})
        usdc_balance = balance['total']['USDC']
        print(f"USDC balance: {usdc_balance}")
        if usdc_balance > capital:
            print("Sufficient USDC balance available. Proceeding..")
            return True
        else:
            print("Insufficient USDC balance. Exiting.")
            exit()
    except Exception as e:
        print(f"An error occurred while fetching the USDC balance: {str(e)}")


# Function to read config file

config = configparser.ConfigParser()
config.read('config.ini')

# Get the API key and secret from the config file
API_KEY = config['API_Keys']['binance_api_key_futures']
API_SECRET = config['API_Keys']['binance_api_secret_futures']

# Get the trading parameters from the config file
symbol = config['Trading_Parameters']['symbol']
market_symbol = config['Trading_Parameters']['market_symbol']
capital = float(config['Trading_Parameters']['capital'])
leverage = int(config['Trading_Parameters']['leverage'])
epoch_time = int(config['Trading_Parameters']['epoch_time'])
debug = config.getboolean('Debug_Prameters', 'debug')

order_value = capital * leverage  # USDC

binance = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})

check_usdc_balance()

if debug:
    specified_epoch_time = time.time() + 10  # 10 seconds from now
    # print(specified_epoch_time)
else:
    specified_epoch_time = epoch_time

# specified_epoch_time = 1716048269

# Convert epoch timestamp to local time
local_time = time.localtime(specified_epoch_time)

# Format local time to HH:MM:SS
formatted_time = time.strftime('%H:%M:%S', local_time)

# Fetch the current market price
price = binance.fetch_ticker(symbol)['last']

# Get the precision for the symbol
precision = get_symbol_precision(symbol)

# Calculate the quantity with the correct precision
quantity = round(order_value / price, precision)

print(f"Execution Scheduled at time: {formatted_time}")
run_at_epoch(specified_epoch_time, excecute_long_and_short)
