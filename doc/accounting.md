# Accounting App

Details for the lightweight double-entry accounting features.

## Models
- `Account` – chart of accounts with type (Asset, Expense, Liability, etc.).
- `Category` – user-defined tags for transactions.
- `Transaction` – a single monetary change posted to two accounts.
- `Journal` – grouping of transactions for imports or batch operations.

## Endpoints
- `GET /api/accounts/` – list and manage accounts.
- `GET /api/transactions/` – list transactions with filters.
- `POST /api/transactions/` – create a new double-entry transaction.
- `POST /api/transactions/import/` – bulk upload from CSV.

## Background Tasks
- Daily summary job to update account balances.
- Optional export of monthly statements via email.
