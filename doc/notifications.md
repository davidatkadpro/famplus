# Notifications App

Central place for user alerts and reminders.

## Models
- `NotificationPreference` – user-specific settings for email/push.
- `Notification` – stored message with read state.

## Endpoints
- `GET /api/notifications/` – list recent notifications for the user.
- `POST /api/notifications/mark-read/` – bulk mark as read.

## Background Tasks
- Celery tasks for sending emails and push notifications.
- Scheduled reminders for due chore approvals or account updates.
