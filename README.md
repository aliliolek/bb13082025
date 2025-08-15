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

Application options are split between a versioned YAML file and private environment variables.

### `config.yaml`

Non‑secret settings live in `config.yaml` at the project root:

```yaml
bybit:
  testnet: false
  recv_window: 20000

polling:
  price: 60
  balance: 300

payments:
  min_match_count: 1
  mappings:
    USDT_UAH: MonoBank
```

Set `bybit.testnet` to `true` to target the Bybit testnet environment. `recv_window` controls the request receive window in milliseconds.

### Environment variables

API credentials and bot secrets are loaded from the environment (or a local `.env` file). Copy `.env.example` to `.env` and fill in the values:

```
BYBIT_API_KEY=<your api key>
BYBIT_API_SECRET=<your api secret>
TG_BOT_TOKEN=<telegram bot token>
TG_ADMIN_ID=<telegram admin id>
```

`BYBIT_API_KEY` and `BYBIT_API_SECRET` authenticate requests to Bybit. `TG_BOT_TOKEN` and `TG_ADMIN_ID` configure the Telegram bot.

## Protected directories (DO NOT EDIT)

The following paths are **reference-only**. They must never be modified by humans or AI tools.

- `examples/` – sample API payloads/responses (ground truth for I/O)
- `scripts/` – project utilities used by CI and local tooling
- `reference_bybit_p2p_lib/` – a pinned copy of the bybit_p2p library

**Codex/Cursor:** You may read these folders to understand the API, but you must not edit, not move, not import or delete anything inside them.
