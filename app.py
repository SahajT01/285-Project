import streamlit as st
import yfinance as yf
import pandas as pd

# Fetching real-time data from Yahoo Finance
def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        return hist['Close'].iloc[-1]  # Gets the latest closing price
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Portfolio allocation logic
def allocate_portfolio(investment, strategies):
    strategy_to_assets = {
        'Ethical Investing': ['AAPL', 'ADBE', 'NSRGY'],
        'Growth Investing': ['AMZN', 'TSLA', 'NVDA'],
        'Index Investing': ['VTI', 'IXUS', 'ILTB'],
        'Quality Investing': ['JNJ', 'PG', 'DIS'],
        'Value Investing': ['IBM', 'JPM', 'WMT']
    }
    assets = []
    for strategy in strategies:
        assets.extend(strategy_to_assets[strategy])
    num_assets = len(assets)
    investment_per_asset = investment / num_assets
    portfolio = {}
    for asset in assets:
        current_price = fetch_data(asset)
        if current_price is not None:
            shares = investment_per_asset / current_price
            portfolio[asset] = {'Investment': investment_per_asset, 'Current Price': current_price, 'Shares': shares}
    return portfolio

# Main page layout
def main():
    st.title('Stock Portfolio Suggestion Engine')
    investment = st.number_input('Enter investment amount in USD', min_value=5000, step=1000)
    strategies = st.multiselect(
        'Select Investment Strategy',
        ['Ethical Investing', 'Growth Investing', 'Index Investing', 'Quality Investing', 'Value Investing'],
        format_func=lambda x: f"{x} - Click for details"
    )

    if strategies:
        st.write("Information on selected strategies:")
        for strategy in strategies:
            if strategy == 'Ethical Investing':
                st.info("Ethical Investing focuses on companies that demonstrate ethical practices.")
            # Add more detailed descriptions for each strategy here...

    if st.button('Generate Portfolio'):
        if not strategies:
            st.error("Please select at least one strategy.")
        else:
            portfolio = allocate_portfolio(investment, strategies)
            st.write("Your portfolio:", portfolio)

            # Optional: Store and display historical values
            df = pd.DataFrame(list(portfolio.values()))
            st.line_chart(df['Current Price'])

if __name__ == "__main__":
    main()