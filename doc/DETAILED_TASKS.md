# Detailed Task Breakdown

This document expands the high-level items in `TASKS.md`.

## Phase 0 – Bootstrap
- Set up the monorepo directories for **backend**, **frontend**, **doc** and **scripts**.
- Configure Python and Node version managers.
- Add Git hooks and linters (black, isort, flake8, prettier, eslint).
- Configure local MySQL and Redis services. Optionally install Mailhog for email testing.
- Create CI workflow on GitHub Actions for linting and tests.

## Phase 1 – Backend Foundation
- Initialise Django project using `django-admin startproject`.
- Place all backend apps under `backend/apps/` for easier organisation.
- Add a `core` app:
  - Custom `User` model using email login.
  - Shared mixins and utility helpers.
- Create a `families` app:
  - `Family` and `Membership` models.
  - Invitation generation and acceptance views.
- Integrate Django REST Framework and simple JWT authentication.
- Implement row-level filtering for `family_id` via DRF permissions and querysets. ✅

## Phase 2 – Domain Apps
### Chores
- Port `Chore` and `Entry` models from the old project.
- Write CRUD API endpoints and approval workflows.
- Schedule Celery tasks for automatic entry creation.

### Accounting
- Define `Account`, `Category`, `Transaction` and `Journal` models.
- Enforce double-entry accounting rules and provide balance helpers.
- Provide import/export endpoints for transactions.

### Assets
- Implement `Asset`, `Price` and `AssetTransactionLink` models.
- Service for fetching prices from CoinGecko.
- Gain strategy calculations (FIFO / LIFO / MAX gain).

### Notifications (optional)
- Email and push notifications for due chores and approvals.

## Phase 3 – Frontend Foundation
- Create a Vite + React + TypeScript workspace.
- Install Tailwind CSS and `shadcn/ui` components.
- Add a theme provider with light and dark modes.
- Configure ESLint and Prettier.
- Set up React Router, TanStack Query and authentication hooks.

## Phase 4 – Frontend Features
- Chore dashboard with approval modals.
- Transaction ledger with category filtering and tagging.
- Asset portfolio table and charts.
- Family administration pages.

## Phase 5 – Polish & Deployment
- Add E2E tests using Playwright or Cypress.
- Review accessibility and internationalisation.
- Build production configuration and Traefik settings.
- Deploy a preview instance (Fly.io, Render or AWS).

## Nice-to-Haves
- Mobile application with React Native / Expo.
- Real-time updates with WebSockets.
- Budget planner and forecasting graphs.
