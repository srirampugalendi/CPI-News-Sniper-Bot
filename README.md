# CPI-News-Sniper-Bot

This Python script provides automated trading functionality on the Binance Futures market. It is designed to execute simultaneous long and short positions at a specified epoch time, allowing traders to capitalize on significant market events like CPI news releases. The script uses the ccxt library to interface with the Binance API, ensuring direct interaction with market data and trading operations.

Features:
Simultaneous Long and Short Positions: Opens both long and short positions at the exact specified time to take advantage of market volatility.
Configurable via INI File: Users can set trading parameters such as capital, leverage, and the target symbol through a configuration file, making the script flexible and easy to adjust without modifying the source code.
Scheduled Execution: Trades are scheduled to execute at a precise epoch time, ensuring timely entry regardless of the script start time.
Leverage Setting: Automatically sets the desired leverage for the trading symbol as specified in the configuration.
Balance Check: Verifies that the account has sufficient USDC balance to proceed with the trading plan, enhancing reliability.
Debug Mode: Includes a debug mode that allows running the script without placing actual orders, useful for testing and verification.

Configuration:
API Keys: Set your Binance Futures API key and secret.
Trading Parameters: Define the trading symbol, capital to use, leverage, and the exact time for order execution.
Debug Parameters: Enable or disable debug mode to run the script without executing real trades.

Requirements:
ccxt Library: Ensure ccxt is installed to interact with cryptocurrency exchanges.
Python Environment: Python 3.x is required.
Binance Account: A Binance account with Futures trading enabled and API keys generated.

Usage:
Setup Configuration File: Populate config.ini with your API credentials, trading parameters, and epoch time for execution.
Install Dependencies: Make sure Python and the ccxt library are installed in your environment.
Run the Script: Execute the script. Ensure your system time is accurate and synchronized for timely execution.
This script is particularly useful for traders looking to automate their strategies around specific market events, minimizing manual intervention and reaction time. Adjust the script as necessary to fit different trading strategies or adapt to other markets beyond Binance Futures.
