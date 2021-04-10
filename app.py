import streamlit
import finnhub
import streamlit as st
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.title('CryptoTracer 💹')
st.sidebar.text("@ your service")
st.sidebar.title('Page Selection Menu')
page = st.sidebar.radio("Select Page:",("StockTracer","CryptoTracer"))
finnhub_client = finnhub.Client(api_key="c1o22fq37fkv6lmc9seg")

if page=="StockTracer":
	st.title('StockTracer - Hackulus 2021 📈📉')
	# Setup client
	


	def matplotlib_plot(chart_type: str, df,i):
	    """ return matplotlib plots """

	    fig, ax = plt.subplots()
	    if i==1:
	    	var = "First"
	    else:
	    	var = "Next"	
	    if chart_type == "Bar":
	        ax.scatter(x=df["Input"],y=df["Output"])

	        plt.title(f"Covid Case Count in US - {var} 25 states")
	        plt.xlabel("State Name")
	        plt.ylabel("Active Cases")
	        plt.tight_layout()

	        plt.ticklabel_format(axis="y",style='plain')
	        plt.xticks(rotation=90)

	    return fig


	# Stock candles
	ticker_symbol = st.text_input("Enter Company Name or Ticker Symbol","Tesla")
	timeframe = st.selectbox("Select Time frame (Optional) ",['D','W', 'M', '1','5', '15', '30', '60'])
	 
	if st.button("Go!"):
		with st.spinner("Fetching Response..."):
			#sleep(5)
			if ticker_symbol == "":
				st.error("Please enter all fields...")
			else:	
				try:
					info = st.beta_expander("Company Details:",expanded=True)
					ticker_symbol = finnhub_client.symbol_lookup(ticker_symbol)
					ticker_symbol = ticker_symbol['result'][0]['symbol']

					# Company details
					company_details = finnhub_client.company_profile2(symbol= ticker_symbol)
					
					company_exchange = company_details["exchange"]
					company_name = company_details["name"]
					company_market_cap = company_details["marketCapitalization"]
					company_ticker = company_details["ticker"]
					company_web_url = company_details["weburl"]
					company_logo = company_details["logo"] 

					
					info.markdown(f"<b>Name</b>: {company_name}",unsafe_allow_html=True)

					col1, col2 = info.beta_columns(2)
					col1.image(company_logo,width = 200)
					col2.title(ticker_symbol)
					
					sleep(2)
					amount = finnhub_client.quote(ticker_symbol)['c']
					col2.subheader("Current Stock Price:")
					col2.title(f"{amount}$")
					
					info.markdown(f"<b>Market Cap</b>: {company_market_cap}",unsafe_allow_html=True)
					info.markdown(f"<b>Ticker Symbol</b>: {company_ticker}",unsafe_allow_html=True)
					info.markdown(f"<b>URL</b>: {company_web_url}",unsafe_allow_html=True)
					info.markdown(f"<b>Exchange</b>: {company_exchange}",unsafe_allow_html=True)
				except:
					st.info("Company details unavailable.")	
			


				# Aggregate Indicators
				# sleep(10)
				
				st.text("")
				# st.text("")
				# st.text("")
				try:
					result = finnhub_client.aggregate_indicator(ticker_symbol, "60")
					count = result['technicalAnalysis']['count']
					buy = count['buy']
					sell = count['sell']
					neutral = count['neutral']

					if buy > sell:
						st.success(f"{ticker_symbol}: Buy > Sell")
					elif buy < sell:
						st.warning(f"{ticker_symbol}: Sell > Buy")	
					elif buy < sell:
						st.info(f"{ticker_symbol}: Buy = Sell")
				except:
					st.info("Technical Analysis Unavailable")		
			
							

				st.text("")
				#st.text("")
				sleep(0.2)
				#st.text("hi")
				try:
					res = finnhub_client.stock_candles(ticker_symbol, timeframe, 1590988249, 1591852249)
					df = pd.DataFrame(res)
					df.rename(columns={'c': 'Close Price', 'h': 'High Price','l': 'Low Price','o': 'Open Price','s': 'Status','t': 'Timestamp','v': 'Volume'}, inplace=True)
					stocks = st.beta_expander("Stock Performance:",expanded=True)
					#st.subheader('Stock Performance')
					stocks.subheader("Analyze Stock Performance:")
					stocks.dataframe(df)
				except:
					st.info("Performance details unavailable ")	

				

				st.text("")
				st.text("")
				st.text("")
				examples = st.beta_expander("Related Buzz News:",expanded=True)
				examples.info("Read related news to better predict macro-shifts in the market!")

				
				sleep(0.2)
				try:
					news = finnhub_client.company_news(ticker_symbol, _from="2020-06-01", to="2020-06-10")

					for x in news[0:2]:
						news = x
						headline = news['headline']
						summary = news['summary']
						examples.subheader(headline)
						examples.image(news['image'], width = 500)
						examples.markdown(summary)
				except:
					st.info("Relevant news unavailable")	

				st.text("")
				st.text("")
				st.text("")	

				cases  = finnhub_client.covid19()	
				dictionary1 = {}
				dictionary2 = {}
				col1 = []
				col2 = []
				for state in cases:
					state_name = state["state"]
					case_count = state["case"]
					col1.append(state_name)
					col2.append(case_count)

				dictionary1['Input'] = col1[:25]
				dictionary1['Output'] = col2[:25]	

				dictionary2['Input'] = col1[25:]
				dictionary2['Output'] = col2[25:]
		    	

				final_df1 = pd.DataFrame(dictionary1)
				final_df2 = pd.DataFrame(dictionary2)

				visualisation = st.beta_expander("Covid Cases Analysis:",expanded=True)
				visualisation.info("Analyse Covid in all 50 states of US to understand current employability condition and make a better stock purchase.")
				plot = matplotlib_plot("Bar",final_df1,1)
				visualisation.pyplot(plot)

				visualisation.write("")
				visualisation.write("")
				visualisation.write("")
				visualisation.write("")
				visualisation.write("")
				visualisation.write("")
				
				plot1 = matplotlib_plot("Bar",final_df2,2)
				visualisation.pyplot(plot1)


elif page=="CryptoTracer":
	st.title("CrytoTracer")
	#api_key1="c1o848a37fkqrr9sbt70"
	#finnhub_client = finnhub.Client(api_key1)
	# ticker_symbol = st.text_input("Enter Company Name or Ticker Symbol","BINANCE")
	ticker_symbol = st.selectbox("Choose Ticker Symbol",[
	 "Binance",
	 "COINBASE",
	 "KRAKEN",
	  "HITBTC",
	  "GEMINI",
	  "POLONIEX",
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
				#try:
				res  = finnhub_client.crypto_candles(ticker_symbol, timeframe, 1590988249, 1591852249)
				df = pd.DataFrame(res)
				df.rename(columns={'c': 'Close Price', 'h': 'High Price','l': 'Low Price','o': 'Open Price','s': 'Status','t': 'Timestamp','v': 'Volume'}, inplace=True)
				cryptic = st.beta_expander("Crypto Performance:",expanded=True)
				#st.subheader('Stock Performance')
				cryptic.subheader("Analyze Crypto Performance:")
				cryptic.info("You can also sort the values")
				cryptic.dataframe(df)
				#except:
					#st.info("Performance details unavailable..Refresh again or change time frame")	
