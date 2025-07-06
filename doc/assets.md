# Assets App

Handles tracking of investments or collectibles.

## Models
- `Asset` – represents an individual asset such as a crypto coin or share.
- `Price` – timestamped value of an asset in a reference currency.
- `AssetTransactionLink` – ties accounting transactions to asset movements.

## Endpoints
- `GET /api/assets/` – list assets in the portfolio.
- `POST /api/assets/` – add a new asset.
- `GET /api/asset-prices/` – retrieve historical price data.
- `POST /api/portfolio/realise/` – compute gains for disposals.

## Background Tasks
- Periodic fetch of latest prices from CoinGecko.
- Gain strategy calculation jobs (FIFO/LIFO/MAX gain).
