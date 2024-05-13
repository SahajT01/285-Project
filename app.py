import streamlit as st
import yfinance as yf
import pandas as pd

# Fetching historical data from Yahoo Finance

# Fetching historical data from Yahoo Finance
def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6d")
        # Ensure the index is tz-naive
        return hist['Close'].tz_localize(None)
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        # Ensure consistent index by using tz-naive
        return pd.Series([None]*6, index=pd.date_range(end=pd.Timestamp.today(), periods=6, freq='D', tz=None))

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
    historical_data = pd.DataFrame()
    total_portfolio_value = pd.Series(0, index=pd.date_range(end=pd.Timestamp.today(), periods=6, freq='D', tz=None))

    for asset in assets:
        closing_prices = fetch_data(asset)
        if closing_prices is not None and not closing_prices.isnull().all():
            current_price = closing_prices.dropna().iloc[-1]
            shares = investment_per_asset / current_price
            portfolio[asset] = {'Investment': investment_per_asset, 'Current Price': current_price, 'Shares': shares}
            historical_values = closing_prices * shares
            historical_data[asset] = historical_values
            total_portfolio_value = total_portfolio_value.add(historical_values, fill_value=0)

    return portfolio, historical_data, total_portfolio_value.iloc[-5:] 
# Main page layout
def main():
    st.title('Stock Portfolio Suggestion Engine')
    investment = st.number_input('Enter investment amount in USD', min_value=5000, step=1000)
    strategies = st.multiselect(
        'Select Investment Strategy',
        ['Ethical Investing', 'Growth Investing', 'Index Investing', 'Quality Investing', 'Value Investing'],
        format_func=lambda x: f"{x} - Click for details"
    )

    if len(strategies) > 2:
        st.error('Please select no more than two strategies.')
        strategies = strategies[:2]  # Limit to two strategies

    if strategies:
        st.write("Information on the first two selected strategies:")
        for strategy in strategies:
            if strategy == 'Ethical Investing':
                st.info("Ethical Investing focuses on companies that demonstrate ethical practices.")

    if st.button('Generate Portfolio'):
        if not strategies:
            st.error("Please select at least one strategy.")
        else:
            portfolio, historical_data, total_portfolio_value = allocate_portfolio(investment, strategies)
            st.write("Your portfolio:", portfolio)

            # Display historical values for all assets in a single chart
            st.write("Historical prices for selected assets (last 5 days):")
            st.line_chart(historical_data)

            # Display the total portfolio value over the last 5 days
            st.write("Total portfolio value over the last 5 days:")
            print(total_portfolio_value)
            st.line_chart(total_portfolio_value)

if __name__ == "__main__":
    main()
