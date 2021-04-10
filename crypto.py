import finnhub
import streamlit as st
from time import sleep
import pandas as pd
import requests

st.title("CrytoTracer")
api_key="c1o848a37fkqrr9sbt70"
finnhub_client = finnhub.Client(api_key)
# ticker_symbol = st.text_input("Enter Company Name or Ticker Symbol","BINANCE")
ticker_symbol = st.selectbox("Enter Company Name or Ticker Symbol",[
 "KRAKEN",
  "HITBTC",
  "COINBASE",
  "GEMINI",
  "POLONIEX",
  "Binance",
  "ZB",
  "BITTREX",
  "KUCOIN",
  "OKEX",
  "BITFINEX",
  "HUOBI"
])
# tokens = requests.get(f'https://finnhub.io/api/v1/crypto/exchange?token={api_key}')
# tokens=tokens.json()
# st.info(tokens)

timeframe = st.selectbox("Select Time frame (Optional) ",['D','W', 'M', '1','5', '15', '30', '60'])


if st.button("Go!"):
	with st.spinner("Fetching Response..."):
		#sleep(5)
		if ticker_symbol == "":
			st.error("Please enter all fields...")
		else:	
			
			
			ticker_symbol = finnhub_client.crypto_symbols(ticker_symbol.upper())
			
			ticker_symbol = ticker_symbol[0]['symbol']


		

			


			st.text("")
			#st.text("")
			sleep(0.2)
			#st.text("hi")
			try:
				res  = requests.get(f'https://finnhub.io/api/v1/crypto/candle?symbol={ticker_symbol}&resolution=D&from=1572651390&to=1575243390&token={api_key}')
				df = pd.DataFrame(res.json())
				df.rename(columns={'c': 'Close Price', 'h': 'High Price','l': 'Low Price','o': 'Open Price','s': 'Status','t': 'Timestamp','v': 'Volume'}, inplace=True)
				stocks = st.beta_expander("Crypto Performance:",expanded=True)
				#st.subheader('Stock Performance')
				stocks.subheader("Analyze Crypto Performance:")
				stocks.dataframe(df)
			except:
				st.info("Performance details unavailable..Refresh again or change time frame")	

