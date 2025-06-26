# 🗂️ FamPlus – High-Level Task Tracker

> Mark items with `[x]` as they are completed.  More granular subtasks and implementation notes will be kept inside the `doc/` folder.

---

## Phase 0 – Bootstrap
- [ ] Create `famplus` monorepo structure (backend, frontend, doc, scripts).
- [ ] Configure Git pre-commit hooks & linters (black, isort, flake8, prettier, eslint).
- [ ] Add Docker Compose with Postgres, Redis & optional Mailhog.
- [ ] Set up CI (GitHub Actions) for test & lint pipelines.

## Phase 1 – Backend Foundation
- [ ] Initialise Django project (`django-admin startproject famplus_backend`).
- [ ] Add **core** app with:
  - [ ] Custom `User` model (email login).
  - [ ] Base mixins & utilities.
- [ ] Implement **families** app:
  - [ ] `Family` model (name, owner, settings).
  - [ ] `Membership` model (role: Parent / Child / Guest).
  - [ ] Invitation & accept flow.
- [ ] Integrate Django REST Framework & simple-jwt.
- [ ] Global row-level filtering by `family_id` via custom DRF permissions & querysets.

## Phase 2 – Domain Apps

### 2.1 Chores
- [ ] Port existing `Chore`, `Entry` logic into new app.
- [ ] REST endpoints for CRUD & approval workflow.
- [ ] Celery tasks for automatic entry spawning.

### 2.2 Accounting
- [ ] Models: `Account`, `Category`, `Transaction`, `Journal`.
- [ ] Double-entry constraints & balance helpers.
- [ ] Endpoint for transaction import/export.

### 2.3 Assets
- [ ] Models: `Asset`, `Price`, `AssetTransactionLink`.
- [ ] Price query service (reuse CoinGecko integration).
- [ ] Gain strategy computation (FIFO / LIFO / MAX gain).

### 2.4 Notifications (optional in v1)
- [ ] Email & push notifications for due chores & approvals.

## Phase 3 – Frontend Foundation
- [ ] Initialise Vite + React + TypeScript workspace.
- [ ] Install Tailwind CSS & shadcn/ui.
- [ ] Add global theme provider (light/dark).
- [ ] Configure ESLint & Prettier.
- [ ] Setup React Router, TanStack Query & JWT auth hooks.

## Phase 4 – Frontend Features
- [ ] Chore dashboard & approval modals.
- [ ] Transaction ledger with category filter/tagging.
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