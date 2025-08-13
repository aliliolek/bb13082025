# Sample App

A minimal Python project skeleton that interacts with the Bybit P2P API.

## Setup and Usage

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
make run
make test
make format
make lint
```

## Configuration

Set the following environment variables or place them in a `.env` file:

```
BYBIT_API_KEY=<your api key>
BYBIT_API_SECRET=<your api secret>
BYBIT_TESTNET=false  # optional
BYBIT_RECV_WINDOW=20000  # optional
```

`BYBIT_TESTNET` should be `true` when using the Bybit testnet environment.

`BYBIT_RECV_WINDOW` controls the request receive window in milliseconds.
