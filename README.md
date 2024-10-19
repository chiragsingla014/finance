# 💸 finance

This project is a web-based application that allows users to simulate trading stocks. It provides features to register accounts, buy and sell stocks, and track transactions and portfolio value. The app uses Python, Flask, and SQLite, and incorporates CS50’s SQL module for database operations. The frontend is built using HTML, CSS (via Bootstrap), and Jinja templates.

## 📋 Project Overview

The application enables users to:
- Register and log in to their accounts.
- Look up stock prices.
- Buy and sell stocks.
- Track their stock portfolio and view transaction history.
- Implement additional features as a personal touch, such as adding more cash to their account or changing passwords.

### Key Features

- 🔐 **User Authentication**: Register, log in, and log out securely.
- 📊 **Stock Lookup**: Search for real-time stock quotes.
- 💸 **Buy & Sell**: Buy and sell stocks, with automated calculations of portfolio value.
- 📜 **Transaction History**: View complete transaction history, including buys and sells.
- 🏦 **Portfolio Management**: Track current stocks, their prices, and the user’s cash balance.
- ⚙️ **Custom Personal Touches**: Add custom features like password changes, adding cash, and more.

## 🏗️ Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:chiragsingla014/finance.git
    cd finance
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the SQLite database by running the schema:
    ```bash
    flask run
    ```

## 🚀 How to Use

1. **Register** for an account or log in if you already have one.
2. Use the **Quote** feature to look up stock prices.
3. Navigate to the **Buy** page to purchase shares of a stock.
4. Use the **Sell** page to sell shares of stocks you own.
5. View your current holdings on the **Home** page.
6. Check your **History** page for all past transactions.

## 🗂️ Files

- **app.py** - Main application file containing all routes and Flask configurations.
- **helpers.py** - Helper functions for tasks such as formatting currency and stock lookups.
- **requirements.txt** - List of required Python packages.
- **static/** - Folder containing CSS files.
- **templates/** - Folder containing HTML templates.
- **finance.db** - SQLite database to store user data, stock transactions, and account information.

## 🧰 Technologies Used

- **Python 🐍** - Backend programming language.
- **Flask** - Lightweight web framework for building the web application.
- **SQLite** - Database for storing user, stock, and transaction data.
- **Jinja** - Templating engine for generating dynamic HTML pages.
- **Bootstrap** - Frontend framework for responsive design.

## 📑 Features to Implement

### 1. Register
- Allows users to create an account by providing a unique username and password.
- Requires password confirmation and hashes passwords for secure storage.
- Checks if the username is already taken and renders an apology if it is.

### 2. Quote
- Allows users to look up the current price of a stock using its symbol.
- Provides a form for users to enter the stock symbol.
- Displays the stock name, symbol, and current price.

### 3. Buy
- Enables users to purchase stocks by entering the stock symbol and the number of shares.
- Checks if the user has sufficient funds to make the purchase.
- Stores transaction details in the database.

### 4. Index (Home)
- Displays the user’s portfolio, showing the stocks owned, number of shares, current price, and total value.
- Shows the user’s current cash balance.
- Calculates the grand total (stocks’ total value + cash balance).

### 5. Sell
- Allows users to sell stocks they own by selecting from a list of stocks they have.
- Requires users to specify the number of shares to sell.
- Ensures users do not sell more shares than they own.

### 6. History
- Displays a complete transaction history, including buys and sells.
- Shows the date and time of each transaction, stock symbol, transaction type, and amount.

### 7. Personal Touch (Optional)
- **Password Management**: Allow users to change their password.
- **Add Cash**: Enable users to add more cash to their account.
- **Quick Buy/Sell on Index**: Let users buy or sell shares directly from the home page.
- **Other**: Any other features of comparable scope.

## 💻 Running the App

1. Start the Flask development server:
    ```bash
    flask run
    ```
2. Visit `http://127.0.0.1:5000` in your web browser to access the app.

## 🤝 Contributing

Contributions are welcome! If you would like to contribute, feel free to open an issue or a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
