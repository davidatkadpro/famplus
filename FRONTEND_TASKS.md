# 🗂️ Front-End Task Board (FamPlus)

> Status: initial draft – update as tasks progress.

## 0. Foundations

- [x] **Lock toolchain** – add `volta` or `engines` field to `package.json` so everyone uses the same Node/Yarn/NPM versions.
- [x] **Convert project to ESM** or keep CommonJS consistently (avoid mixed warnings).
- **Vite config** –
  - [x] Alias `@/` → `src/`.
  - [x] Proxy `/api` → backend (reads `VITE_API_URL`).
  - [x] Enable React Fast-Refresh in tests.
- [x] **ESLint / Prettier** – export shadcn rules, add CI script (`npm run lint`).
- [x] **Vitest / React-Testing-Library** basic setup.

## 1. Styling & Theming

- [x] Verify `tailwind.config.ts` – extend brand colours, dark-mode class.
- [x] Import Tailwind base in `src/index.css` (it's missing in prod build?).
- [ ] Migrate all components to shadcn/ui primitives (buttons, inputs, table, card).
- [x] Implement system / manual theme switcher in `theme-provider.tsx`.

## 2. Global Providers (App.tsx)

- [x] Wrap the app in `QueryClientProvider` – create `src/lib/reactQuery.ts`.
- [x] Add `Toaster` from shadcn/ui for notifications.
- [x] Error boundary component.
- [x] React Router v6 layout route pattern (`/app/*`).

## 3. API Layer (`src/lib/api.ts`)

- [x] Read base URL from `import.meta.env.VITE_API_URL`.
- [x] Axios instance with JWT interceptor (refresh on 401).
- [x] Helper `typedFetch` for non-axios calls.

## 4. Auth Flow

- [x] `useAuth` hook: login, logout, refreshToken.
- [x] Persist token in `localStorage` + in-memory cache.
- [x] Protect routes with `<RequireAuth />`.

## 5. Feature Slices

### 5.1 Assets
- [x] Fix Chart.js register logic (`Chart.register(...)`).
- [ ] Convert date adapter import to dynamic `import()` to reduce bundle size.
- [x] Handle loading / error states.
- [x] Virtual Exchange: backend models, matching service, API endpoints, React hooks & UI (/app/exchange).

### 5.2 Chores
- [x] Data table using shadcn `DataTable` pattern.
- [x] Mutations: create / complete / approve chore.

### 5.3 Families
- [x] Invitation flow UI (send, accept).
- [x] Role badges component.

### 5.4 Transactions
- [ ] Virtualised ledger list.
- [ ] Formik + Zod powered new-transaction form.

## 6. Accessibility & UX

- [ ] Keyboard nav, aria-labels on interactive components.
- [ ] Colour-contrast checks for both themes.

## 7. Performance

- [ ] Split vendor chunks in Vite config.
- [ ] Lazy-load feature bundles with `React.lazy` + `Suspense`.

## 8. PWA / Mobile

- [ ] Add manifest & icons.
- [ ] Service-worker with Vite-PWA.

## 9. Deployment

- [ ] Build script `npm run build && vite preview --port 4173` for prod preview.
- [ ] Upload artefact in GitHub Actions – attach to backend workflow.

---

### How to use this file

1. Open a new branch per task (`feat/frontend-auth`) and link the checkbox.
2. Keep the list sorted; feel free to add bullets.
3. ✅ = done, ❌ = blocked, 🚧 = in-progress.

Happy hacking! 🎨 