import sqlite3
from datetime import datetime
import yfinance as yf


def collect_iv_data():
    stocks = [
        "AAPL", "ABNB", "AI", "AMD", "AMZN", "ARKK", "BABA", "COIN", "DIS", "GDX",
        "GOOGL", "JPM", "MARA", "META", "MRNA", "MSFT", "MSTR", "NFLX", "NVDA",
        "PLTR", "PYPL", "SMCI", "SNOW", "TSLA", "TSM", "XOM"
    ]

    db_file = "iv_data.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS iv_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        stock TEXT NOT NULL,
        atm_iv REAL,
        error TEXT
    )
    ''')
    conn.commit()

    # Fetch and insert data
    for stock in stocks:
        try:
            ticker = yf.Ticker(stock)
            exp_dates = ticker.options  # Get option expiration dates

            # Check if expiry dates are available
            if not exp_dates:
                cursor.execute(
                    "INSERT INTO iv_data (date, stock, atm_iv, error) VALUES (?, ?, ?, ?)",
                    (datetime.now().strftime("%Y-%m-%d"), stock, None, "No options data available")
                )
                continue

            # Choose the first expiry date and fetch the options chain
            first_expiry = exp_dates[0]
            options_chain = ticker.option_chain(first_expiry)
            current_price = ticker.history(period='1d')['Close'].iloc[-1]
            calls = options_chain.calls

            # Find ATM option
            atm_calls = calls.iloc[(calls['strike'] - current_price).abs().argsort()[:1]]
            atm_iv = atm_calls['impliedVolatility'].values[0]

            # Insert data into the database
            cursor.execute(
                "INSERT INTO iv_data (date, stock, atm_iv, error) VALUES (?, ?, ?, ?)",
                (datetime.now().strftime("%Y-%m-%d"), stock, atm_iv, None)
            )

        except Exception as e:
            # Insert error details into the database
            cursor.execute(
                "INSERT INTO iv_data (date, stock, atm_iv, error) VALUES (?, ?, ?, ?)",
                (datetime.now().strftime("%Y-%m-%d"), stock, None, str(e))
            )

    conn.commit()
    conn.close()

    print("Data collection completed and saved to the SQLite database.")
