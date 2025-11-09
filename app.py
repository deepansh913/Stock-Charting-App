import streamlit as st 
from datetime import date
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("📈 Stock Charting App with Range Bar")
st.header("Select the duration and date range")

# Duration selection
duration = st.selectbox("Choose the duration", ["1d", "1mo", "2mo", "3mo"])

# Date range selection
start_date = st.date_input("Start Date", value=date(2024, 1, 1))
end_date = st.date_input("End Date", value=date.today())

# Stock input
stock = st.text_input("Enter stock symbol (e.g. AAPL, TSLA, GOOGL):")

if stock:
    ticker = yf.Ticker(stock)
    
    # Download data
    s = ticker.history(start=start_date, end=end_date)
    
    if not s.empty:
        st.subheader(f"Showing data for {stock.upper()}")
        st.dataframe(s.tail())

        # Create candlestick chart
        data = s.reset_index()
        c_stick_fig = go.Figure(
            data=[go.Candlestick(
                x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
            )]
        )

        # Update layout with range bar
        c_stick_fig.update_layout(
            title=f"{stock.upper()} Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=True,  # 👈 this adds the range slider
            template="plotly_dark",          # dark theme (optional)
            height=600
        )

        st.plotly_chart(c_stick_fig, use_container_width=True)
    else:
        st.warning("No data found for that symbol in the given range.")

    st.write("Technical Indicators")
    delta = s["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    s["RSI"] = 100 - (100 / (1 + rs))
    st.line_chart(s["RSI"])
    st.write("stock buy by the people")
    ticker.recommendations


