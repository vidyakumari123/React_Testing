# GitHub User Finder

A compact **React + TypeScript** single-page app that looks up **GitHub users** by username and shows a **profile card** plus up to **six** most recently updated **public repositories**. It is built with **Vite** and doubles as a **testing workshop**: **Vitest**, **React Testing Library**, and optional **TestSprite MCP** for AI-assisted browser E2E.

---

## Table of contents

- [Why this project](#why-this-project)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting started](#getting-started)
- [Scripts](#scripts)
- [How the app works](#how-the-app-works)
- [UI map (components)](#ui-map-components)
- [Project structure](#project-structure)
- [Testing](#testing)
  - [Unit & component tests (Vitest)](#unit--component-tests-vitest)
  - [End-to-end & TestSprite](#end-to-end--testsprite)
- [Linting & quality](#linting--quality)
- [Build & preview](#build--preview)
- [Troubleshooting](#troubleshooting)
- [Contributing / learning path](#contributing--learning-path)

---

## Why this project

- Practice **testing at the right levels**: pure utilities, isolated components, async hooks with **mocked `fetch`**, and optional **real-browser** flows.
- Keep the **domain simple** (public GitHub REST API) so tests stay readable and the product behavior is easy to reason about.
- Experiment with **TestSprite MCP** in Cursor to generate **Playwright (Python)** journeys against a running dev or preview server.

---

## Features

| Area | Behavior |
| --- | --- |
| Search | GitHub username field with **submit**; **empty submit** shows inline validation (“Please enter a GitHub username.”). |
| Loading | Dedicated loading UI while profile/repos are fetched. |
| Errors | **404** → user-not-found copy; **other HTTP errors** → generic retry message; **network** → connection message; **Try Again** resets state. |
| Profile | Avatar, optional **name**, **`@login`** link to GitHub, optional bio & location, **Repos / Followers / Following** with formatted numbers. |
| Repositories | Up to **six** repos (**`sort=updated`**, `per_page=6`); stars and language dot + label; **“No description provided”** when description is null. |
| Empty state | Shown before any successful search; returning after **clear (×)** calls **`reset`** so results disappear (see `SearchBar` + `App`). |

---

## Tech stack

| Area | Choice |
| --- | --- |
| UI | React 19 |
| Language | TypeScript |
| Bundler / dev server | Vite 8 |
| Unit / component tests | Vitest 4 |
| DOM assertions & rendering | `@testing-library/react`, `@testing-library/jest-dom` |
| User interaction in tests | `@testing-library/user-event` |
| Test environment | jsdom |
| Linting | ESLint 10 (+ TypeScript ESLint, React Hooks, React Refresh) |
| Coverage | `@vitest/coverage-v8` |
| Optional AI / browser E2E | [TestSprite](https://www.testsprite.com/) MCP — generated scripts live under [`testsprite_tests/`](./testsprite_tests/README.md) |

---

## Prerequisites

- **Node.js** — use an LTS version your team agrees on; **TestSprite MCP** often expects **Node 22+** (see [Troubleshooting](#troubleshooting)).
- **npm** (bundled with Node).

---

## Getting started

```bash
git clone <your-fork-or-repo-url>
cd react-testing-course
npm install
npm run dev
```

Open **http://localhost:5173** (Vite default). Try usernames such as **`octocat`** for a reliable public profile.

---

## Scripts

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start Vite dev server with HMR (default port **5173**). |
| `npm run build` | Typecheck (`tsc -b`) + production bundle → **`dist/`**. |
| `npm run preview` | Serve **`dist/`** locally (good for production-like checks and TestSprite). |
| `npm run lint` | Run ESLint across the repo. |
| `npm test` | Vitest in **watch** mode. |
| `npm test -- --run` | Vitest **single run** (CI-style). |
| `npm run coverage` | Vitest with **v8 coverage** → **`coverage/`** HTML report. |

---

## How the app works

1. **`App.tsx`** composes the shell: header, **`SearchBar`**, then either loading, error, empty state, or **`UserCard`** + **`RepoList`**.
2. **`useGithubUser`** (`src/hooks/useGithubUser.ts`) owns remote data:
   - `GET https://api.github.com/users/{username}`
   - `GET https://api.github.com/users/{username}/repos?sort=updated&per_page=6`  
   No GitHub token is required for these public endpoints; **[rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)** still apply (stricter when unauthenticated).
3. **`SearchBar`** calls **`onSearch(username)`** on valid submit and optional **`onClear()`** when the user clears the input—**`App`** passes **`reset`** so the UI returns to the empty state after ×.
4. **Types** for API payloads live in **`src/types/github.ts`**.
5. **`formatNumber`** (`src/utils/formatNumber.ts`) keeps large follower/repo counts readable in **`UserCard`**.

### API outcomes

| Situation | User-visible result |
| --- | --- |
| User missing (**404**) | Message like *User `"…"` not found on GitHub.* |
| Other non-OK HTTP | *Something went wrong. Please try again.* |
| `fetch` throws | *Network error. Please check your connection.* |

---

## UI map (components)

| Component | Role |
| --- | --- |
| `SearchBar` | Controlled input, validation alert, Search button (spinner when loading), clear ×, **`onClear`** hook-up |
| `LoadingState` | Shown while `loading` is true |
| `ErrorMessage` | Alert + **Try Again** → `reset` |
| `UserCard` | Profile summary and stats |
| `RepoList` | Section title + grid or “No public repositories” |
| `RepoItem` | Single repo card (link, stars, language) |

---

## Project structure

```text
react-testing-course/
├── public/                    # Static assets
├── src/
│   ├── components/            # UI + colocated *.test.tsx
│   ├── hooks/                 # useGithubUser + tests
│   ├── utils/                 # formatNumber + tests
│   ├── types/                 # GithubUser, GithubRepo
│   ├── test/
│   │   ├── setup.ts           # jest-dom + RTL cleanup
│   │   └── mocks.ts           # Shared fixtures for tests
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── index.css
├── testsprite_tests/          # TestSprite-generated Playwright (Python) E2E — see testsprite_tests/README.md
├── index.html
├── vite.config.ts             # Vite + Vitest
├── eslint.config.js
├── tsconfig*.json
├── package.json
└── README.md
```

---

## Testing

### Unit & component tests (Vitest)

Approach: **test behavior, not implementation**—query the DOM the way users and assistive tech encounter it (roles, labels, text). Hook logic is covered with **`fetch`** mocked so tests do not depend on GitHub uptime.

**Included tooling**

- **Vitest** — same pipeline as Vite, fast watch, ESM-friendly.
- **jsdom** — DOM APIs in Node for components.
- **React Testing Library** — render, query, `user-event` for interactions.
- **`@testing-library/jest-dom`** — matchers (`toBeInTheDocument`, …) via `src/test/setup.ts`.
- **`cleanup`** after each test to avoid leaking DOM between cases.

**Vitest config** (`vite.config.ts`): `globals`, `environment: "jsdom"`, `setupFiles: "./src/test/setup.ts"`.

**Spec files**

| File | Focus |
| --- | --- |
| `src/components/SearchBar.test.tsx` | Validation, submit, **`onClear`**, loading/disabled |
| `src/components/UserCard.test.tsx` | Profile fields, conditional sections |
| `src/components/RepoList.test.tsx` | Grid vs empty repos |
| `src/components/RepoItem.test.tsx` | Repo row, language, null description |
| `src/hooks/useGithubUser.test.tsx` | Success path, 404, HTTP errors, network error |
| `src/utils/formatNumber.test.ts` | Formatting edge cases |

Fixtures: **`src/test/mocks.ts`** (`mockUser`, `mockUserMinimal`, `mockRepos`).

**Commands**

```bash
npm test                    # watch mode
npm test -- --run           # CI single run
npm test -- --run src/components/SearchBar.test.tsx
npm run coverage            # opens coverage/index.html after generation
```

**Practices when extending tests**

1. Prefer **`getByRole`**, **`getByLabelText`**, **`getByText`** over CSS or XPath.
2. Use **`findBy*`** / **`waitFor`** when UI updates asynchronously after an action.
3. Mock **`globalThis.fetch`** in hook tests; avoid live API calls in unit tests.
4. Centralize shared JSON fixtures in **`src/test/mocks.ts`**.

---

### End-to-end & TestSprite

| Layer | What runs | Where |
| --- | --- | --- |
| Default automated checks | Vitest + jsdom | `npm test` |
| AI-generated browser E2E | Playwright (**Python**) against **`http://localhost:5173`** | [`testsprite_tests/`](./testsprite_tests/README.md) |

**TestSprite** ([docs overview](https://docs.testsprite.com/mcp/getting-started/overview)) connects Cursor (and similar editors) to an agent that can summarize the codebase, build a **frontend test plan**, emit **Playwright** scripts (**`TC001`–`TC015`**), run them, and write reports such as **`testsprite_tests/testsprite-mcp-test-report.md`**. Flows hit the **real GitHub API** unless you later rewrite tests to stub network calls.

**Typical MCP workflow**

1. Start the app: **`npm run dev`** or, for stability under load, **`npm run build && npm run preview`** (still typically port **5173**).
2. In Cursor, enable **TestSprite MCP** and prompt e.g. *“Help me test this project with TestSprite”* or ask for E2E coverage for this finder app.
3. If **`engines.node >= 22`** is required by the MCP package, use **Node 22+** and restart the editor if you see **`EBADENGINE`** or MCP timeouts.

More detail: **[`testsprite_tests/README.md`](./testsprite_tests/README.md)** (Python deps, `playwright install chromium`, running a single `TC*.py`).

---

## Linting & quality

```bash
npm run lint
```

Configuration lives in **`eslint.config.js`**. Enable ESLint in your editor for immediate feedback on hooks dependencies, refresh rules, and TypeScript-aware rules where configured.

---

## Build & preview

```bash
npm run build    # produces dist/
npm run preview  # serve dist/ for smoke-testing production assets
```

---

## Troubleshooting

| Symptom | Things to check |
| --- | --- |
| **GitHub rate limit** or flaky searches | Unauthenticated REST limits are low; wait or use a token in a fork if you extend the hook to send `Authorization`. |
| **TestSprite MCP** `EBADENGINE` / fails to start | Upgrade to **Node 22+**; reinstall MCP after switching Node. |
| **MCP connection timeout** | Ensure **`npm run dev`** (or preview) is running on the expected port; check firewall/VPN. |
| **Vitest / jsdom quirks** | Confirm **`src/test/setup.ts`** runs (`setupFiles` in `vite.config.ts`). |
| **`coverage/` clutter** | Add **`coverage/`** to `.gitignore` if you do not commit reports. |

---

## Contributing / learning path

Suggested reading order for the test suite:

1. **`formatNumber.test.ts`** — pure functions, no React.
2. **`SearchBar.test.tsx`** — forms, validation, **`onClear`**.
3. **`useGithubUser.test.tsx`** — async state, mocked **`fetch`**.
4. **`RepoItem` / `RepoList` / `UserCard`** — composed UI and conditional rendering.

---

Originally scaffolded from the **Vite React + TypeScript** template; extended into a **GitHub User Finder** demo focused on **testing** and optional **TestSprite** E2E.
