from bybit_p2p import P2P
from dotenv import load_dotenv
import os

load_dotenv() 

def get_api():
    return P2P(
        testnet=False,  
        api_key=os.environ["BYBIT_API_KEY"],
        api_secret=os.environ["BYBIT_API_SECRET"],
        recv_window=20000
    )

