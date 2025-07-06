# 🗂️ FamPlus – High-Level Task Tracker

> Mark items with `[x]` as they are completed.  More granular subtasks and implementation notes will be kept inside the `doc/` folder.

---

## Phase 0 – Bootstrap
- [x] Create `famplus` monorepo structure (backend, frontend, doc, scripts).
- [x] Configure Git pre-commit hooks & linters (black, isort, flake8, prettier, eslint).
- [x] Configure local MySQL and Redis services (no Docker) with optional Mailhog.
- [x] Set up CI (GitHub Actions) for test & lint pipelines.

## Phase 1 – Backend Foundation
- [x] Initialise Django project (`django-admin startproject famplus_backend`).
- [x] Add **core** app with:
  - [x] Custom `User` model (email login).
  - [x] Base mixins & utilities.
- [x] Implement **families** app:
  - [x] `Family` model (name, owner, settings).
  - [x] `Membership` model (role: Parent / Child / Guest).
  - [x] Invitation & accept flow.
- [x] Integrate Django REST Framework & simple-jwt.
- [x] Global row-level filtering by `family_id` via custom DRF permissions & querysets.

## Phase 2 – Domain Apps

### 2.1 Chores
- [x] Port existing `Chore`, `Entry` logic into new app.
- [x] REST endpoints for CRUD & approval workflow.
- [x] Celery tasks for automatic entry spawning.

### 2.2 Accounting
- [x] Models: `Account`, `Category`, `Transaction`, `Journal`.
- [x] Double-entry constraints & balance helpers.
- [x] Endpoint for transaction import/export.

### 2.3 Assets
- [x] Models: `Asset`, `Price`, `AssetTransactionLink`.
- [x] Price query service (reuse CoinGecko integration).
- [x] Gain strategy computation (FIFO / LIFO / MAX gain).

### 2.4 Notifications (optional in v1)
- [x] Email & push notifications for due chores & approvals.

## Phase 3 – Frontend Foundation
- [x] Initialise Vite + React + TypeScript workspace.
- [x] Install Tailwind CSS & shadcn/ui.
- [x] Add global theme provider (light/dark).
- [x] Configure ESLint & Prettier.
- [x] Setup React Router, TanStack Query & JWT auth hooks.

## Phase 4 – Frontend Features
- [x] Chore dashboard & approval modals.
- [x] Transaction ledger with category filter/tagging.
- [ ] Asset portfolio table & charts.
- [ ] Family administration pages.

## Phase 5 – Polish & Deployment
- [ ] Add E2E tests (Playwright / Cypress).
- [ ] Accessibility & i18n review.
- [ ] Create production Dockerfiles & Traefik config.
- [ ] Deploy preview instance to Fly.io / Render / AWS.

---

## Nice-to-Haves / Stretch Goals
- [ ] Mobile app (React Native / Expo).
- [ ] Real-time updates with WebSockets.
- [ ] Budget planner & forecasting graphs.

---

**Next Steps:**
1. Complete Phase 0 bootstrap tasks.
2. Document detailed subtasks in `doc/` directory (one file per bounded context). 