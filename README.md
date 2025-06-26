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
| **Backend**| Django 5 · Django REST Framework · PostgreSQL · Celery/Redis · Strawberry GraphQL (optional) |
| **Frontend**| React 18 + Vite + TypeScript · Tailwind CSS · shadcn/ui · TanStack Query |
| **DevOps**| Docker Compose · GitHub Actions CI · Traefik / Caddy for HTTPS |

---

## 4. Planned Repository Structure
```text
famplus/
├── backend/                 # Django project & apps
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

## 6. Getting Started (to be completed later)
1. Clone repo → `git clone ...`
2. Run bootstrap script → `./scripts/bootstrap.sh`
3. `make up` to start Docker stack.

Detailed instructions will be added once the scaffolding tasks are finished.

---

## 7. Roadmap
High-level tasks are tracked in [`TASKS.md`](TASKS.md).  Sub-tasks & in-depth design notes live under [`doc/`](doc/).

Happy hacking! ✨ 