import streamlit as st
from utils import StockFetch

st.set_page_config(page_title="Stock Market", page_icon="📈")

@st.cache_resource
def get_stock_client(api_key):
    return StockFetch(api_key=api_key)

api_key = st.secrets["API_KEY"]
client = get_stock_client(api_key)

@st.cache_data(ttl=3600)
def search_stock(company):
    return client.search(company = company)

@st.cache_data(ttl=3600)
def plot_chart(symbol):
    return client.plot_candlestick(symbol= symbol)

if __name__ == "__main__":
    st.title("Stock Market Project - Utkarsh")
    company = st.text_input("Please enter company name : ")
    
    if company:
        search_data = search_stock(company)
        if search_data:
            options = st.selectbox("Select Company Symbol", list(search_data.keys()))
            symbol_data = search_data.get(options)
            st.success(f"Company name : {symbol_data[0]}")
            st.success(f"Type : {symbol_data[1]}")
            st.success(f"Region : {symbol_data[2]}")

            if st.button("Submit"):
                fig = plot_chart(symbol=options)
                st.plotly_chart(fig)

        else:
            st.error("No Matching Company Name Found")


