# FamPlus – Next-Generation Family Management Platform

## 1. Purpose
FamPlus is the successor to the existing **banking** app. It retains the proven ideas of chore tracking, allowance automation and simple finance management, but is rebuilt from the ground up for scalability, modularity and multi-family usage.

The project is organised as a **monorepo** with clearly separated _backend_ and _frontend_ packages and a shared documentation space.  
Everything is open-source and designed for self-hosting or simple cloud deployment.

---

## 2. High-Level Feature Set

### Chore Management ✔︎
* Create one-off or recurring chores with flexible schedules.
* Mobile-first dashboard for parents & kids.
* Approval workflow, streaks, points & allowance automation.

### Accounting Lite 💰
* Double-entry style accounts (Asset / Expense / Liability / Equity / Revenue) inspired by current implementation.
* Transaction categorisation with parent-defined _Categories_ and automatic suggestions.
* Family budgets & simple reports.

### Asset Tracking 📈
* Register purchases & disposals of assets (e.g. crypto, shares, collectibles).
* Real-time price look-ups via CoinGecko (or other providers).
* Capital-gain calculation using FIFO / LIFO / Highest-gain strategies.

### Multi-Family Support 👨‍👩‍👧‍👦
* Each **Family** is an isolated tenant; all data rows carry `family_id` and queries are automatically filtered.
* Invitation & role system (Parent, Child, Guest).

### Notifications & Scheduling 🔔
* Server-side tasks (Celery + Redis) for chore spawning, reminders and price refresh.
* Optional push & email integrations.

---

## 3. Technology Stack

| Layer      | Technology |
| ---------- | ---------- |
| **Backend**| Django 5.2 · Django REST Framework · MySQL · Channels 4.1 · Daphne 4.1 · Celery[redis] 5.4 |
| **Frontend**| React 18.3 + Vite + TypeScript · Tailwind CSS · shadcn/ui · TanStack Query 5.21 · lucide-react · axios |
| **DevOps**| Local MySQL & Redis (no Docker) · GitHub Actions CI · Traefik / Caddy for HTTPS |
### Key Package Versions

**Backend**
- Django 5.2
- sqlparse 0.5.3
- mysqlclient 2.2.7
- channels 4.1.0
- daphne 4.1.0
- redis 5.0.4
- celery[redis] 5.4.0

**Frontend**
- react 18.3.0
- react-dom 18.3.0
- react-router-dom 6.23.0
- @tailwindcss/vite 4.1.10
- @tanstack/react-query 5.21.0
- lucide-react 0.300.0
- axios 1.6.5
- shadcn@latest


---

## 4. Planned Repository Structure
```text
famplus/
├── backend/                 # Django project & apps
│   # All Django apps live inside the `apps/` folder
│   ├── manage.py
│   ├── requirements.txt
│   ├── project/             # Django settings
│   └── apps/
│       ├── core/            # Common utilities & custom user model
│       ├── families/        # Multi-tenancy & invitations
│       ├── chores/
│       ├── accounting/
│       └── assets/
├── frontend/                # React/Vite workspace
│   ├── index.html
│   ├── vite.config.ts
│   └── src/
│       ├── components/
│       ├── lib/
│       └── features/
├── doc/                     # Detail design docs & ADRs
└── scripts/                 # Helper shell scripts
```
(Exact layout will evolve as tasks are completed.)

---

## 5. Architectural Notes
1. **Modularity first** – each bounded-context gets its own Django app & React feature slice.  
2. **Strict API contract** – REST/JSON as default, GraphQL considered for complex querying.  
3. **Multi-tenancy** – row-level security enforced through `FamilyForeignKey` and DRF permission classes.  
4. **Dark & Light mode** – shadcn/ui components with system preference toggle.

---

## 6. Getting Started
1. Clone repo → `git clone <this repo>`
2. Install Python & Node requirements.
3. Run service helper → `./scripts/setup_services.sh` (installs & starts MySQL/Redis and optional MailHog).
4. Install pre‑commit → `pip install pre-commit` then `pre-commit install`.
5. Run the dev server → `cd backend && python manage.py runserver`.

---

## 7. Roadmap
High-level tasks are tracked in [`TASKS.md`](TASKS.md).  Sub-tasks & in-depth design notes live under [`doc/`](doc/).

Happy hacking! ✨ 