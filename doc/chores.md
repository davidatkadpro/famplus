# Chores App

Detailed breakdown of the chores domain.

## Models
- `Chore` – template describing the task, schedule and point value.
- `Entry` – individual occurrence of a chore with a `status` field.
  Possible states: `awaiting`, `completed`, `approved`, `rejected`, `achieved`.

## Endpoints
- `GET /api/chores/` – list and filter chores.
- `POST /api/chores/` – create a new chore.
- `PATCH /api/chores/{id}/` – update or archive a chore.
- `POST /api/chore-entries/` – log completion of a chore entry.
- `POST /api/chore-entries/{id}/approve/` – parent approval action.
- `POST /api/chore-entries/{id}/reject/` – reject a completed entry.

## Background Tasks
- Celery beat job spawns `Entry` records based on each `Chore`'s schedule.
- Reminder emails or push notifications for due chores.
