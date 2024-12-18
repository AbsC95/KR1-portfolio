# main.py
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import time

# Data
data = {
    "Crypto": [
        "Ethereum (ETH)", "Polkadot (DOT)", "Internet Computer (ICP)",
        "Cosmos (ATOM)", "Lido (LDO)", "Celestia (TIA)", "Astar (ASTR)",
        "RocketPool (RPL)", "Kusama (KSM)", "Moonbeam (GLMR)", "Moonriver (MOVR)",
        "Bluzelle (BLZ)", "Nym (NYM)", "Acala (ACA)", "Clover (CLV)",
        "Enzyme Finance (MLN)", "Automata Network (ATA)", "Swarm (BZZ)",
        "Vega Protocol (VEGA)", "Shiden (SDN)", "Karura (KAR)", "Etherisc (DIP)",
        "USD Coin (USDC)"
    ],
    "Holding": [
        5427, 5137231, 152352, 1914838, 12000000, 7500000, 68388411, 199779,
        60922, 15991169, 60717, 3659928, 4285719, 11980568, 625000, 28570,
        13348983, 844328, 842494, 577511, 1171859, 1344071, 2731098
    ],
}

coingecko_ids = [
    "ethereum", "polkadot", "internet-computer", "cosmos", "lido-dao",
    "celestia", "astar", "rocket-pool", "kusama", "moonbeam", "moonriver",
    "bluzelle", "nym", "acala", "clover-finance", "melon",
    "automata", "swarm", "vega-protocol", "shiden", "karura",
    "etherisc", "usd-coin"
]

def fetch_prices():
    """Fetch current cryptocurrency prices from CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coingecko_ids), 
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch prices: {e}")
        return {}

def calculate_portfolio_value():
    """Calculate current portfolio value."""
    prices = fetch_prices()
    df = pd.DataFrame(data)
    df["Price (USD)"] = [prices.get(coin_id, {}).get("usd", 0) for coin_id in coingecko_ids]
    df["Total Value (USD)"] = df["Holding"] * df["Price (USD)"]
    total_value = df["Total Value (USD)"].sum()
    return df, total_value

def main():
    st.title("KR1 Portfolio Tracker")
    
    # Initialize session state
    if "portfolio_history" not in st.session_state:
        st.session_state.portfolio_history = pd.DataFrame(columns=["Timestamp", "Total Portfolio Value"])
    
    # Fetch portfolio value
    if st.button("Fetch Current Portfolio Value"):
        df, total_value = calculate_portfolio_value()
        st.session_state.portfolio_history = pd.concat([
            st.session_state.portfolio_history,
            pd.DataFrame({"Timestamp": [datetime.now()], "Total Portfolio Value": [total_value]})
        ]).reset_index(drop=True)
        st.dataframe(df)
        st.write(f"**Current Portfolio Value:** ${total_value:,.2f}")
    
    # Portfolio history graph
    if not st.session_state.portfolio_history.empty:
        fig = px.line(
            st.session_state.portfolio_history,
            x="Timestamp",
            y="Total Portfolio Value",
            title="Portfolio Value Over Time",
            labels={"Total Portfolio Value": "Portfolio Value (USD)"}
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
