# GitHub User Finder

A small React + TypeScript app that searches GitHub profiles by username and shows the user card plus their most recently updated public repositories (up to six). Built with Vite as a playground for component tests, hooks, and utilities using **Vitest** and **React Testing Library**.

## Features

- **Search** GitHub users by username (form validation for empty input)
- **Loading** state while fetching
- **Error** handling for 404 (“user not found”), other API errors, and network failures—with **Try Again** to reset
- **User card**: avatar, name (when present), `@login`, bio, location, formatted stats (repos / followers / following)
- **Repository list**: recent repos with stars and language badge (or fallback copy when description or language is missing)
- **Empty state** when no search has run yet

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
| Optional E2E / AI test workflows | [**TestSprite**](https://www.testsprite.com/) MCP in Cursor (or similar IDEs)—see [Testing → TestSprite](#testsprite-mcp) |

## Prerequisites

- **Node.js** (LTS recommended; match what your team uses)
- **npm** (ships with Node)

## Getting started

```bash
# Install dependencies
npm install

# Start dev server (default: http://localhost:5173)
npm run dev
```

Other useful commands:

```bash
npm run build    # Typecheck + production build → dist/
npm run preview # Serve dist/ locally to verify production build
npm run lint    # ESLint on the repo
```

## How the app works

1. **`App.tsx`** orchestrates UI: search bar, loading, errors, empty state, then `UserCard` + `RepoList` when data is loaded.
2. **`useGithubUser`** (`src/hooks/useGithubUser.ts`) calls the public GitHub REST API—no auth required for basic profile/repo reads, but **[rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)** apply (authenticated requests get higher limits).
   - `GET https://api.github.com/users/{username}`
   - `GET https://api.github.com/users/{username}/repos?sort=updated&per_page=6`
3. **Components** live under `src/components/`; shared types are in `src/types/github.ts`.
4. **Formatting** for large follower/repo counts uses `src/utils/formatNumber.ts`.

### API behavior (good to know)

- **404**: Shows a clear “user not found” message.
- **Other non-OK responses**: Generic “something went wrong” message.
- **Network errors**: Connection-oriented message.

## Project structure

```text
react-testing-course/
├── public/                 # Static assets (e.g. favicon)
├── src/
│   ├── components/         # UI + *.test.tsx colocated with components
│   ├── hooks/              # useGithubUser + hook tests
│   ├── utils/              # Pure helpers + unit tests
│   ├── types/              # GithubUser, GithubRepo
│   ├── test/
│   │   ├── setup.ts        # Vitest + Testing Library global setup
│   │   └── mocks.ts        # Shared mock users/repos for tests
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── index.css
├── index.html
├── vite.config.ts          # Vite + Vitest configuration
├── tsconfig*.json
├── eslint.config.js
├── package.json
└── README.md
```

## Testing

This repo focuses on **fast, deterministic tests** close to how users interact with the UI: render components, query by roles/labels/text, and assert behavior. The custom hook is tested via a tiny wrapper component or by exercising it through the behaviors it drives.

### Stack in this project

- **Vitest** — test runner aligned with Vite (ESM-friendly, fast watch mode).
- **jsdom** — browser-like DOM in Node for component tests (no real browser window).
- **React Testing Library** — encourages queries that resemble accessibility and user-visible output.
- **`@testing-library/jest-dom`** — matchers like `toBeInTheDocument()` (wired in via `src/test/setup.ts`).
- **`@testing-library/user-event`** — realistic keyboard/pointer simulation where needed.

### Global test setup (`src/test/setup.ts`)

- Imports `@testing-library/jest-dom/vitest` so jest-dom matchers are available.
- Calls `cleanup()` after each test so DOM state does not leak between cases.

### Vitest configuration (`vite.config.ts`)

- **`globals: true`** — `describe`, `it`, `expect`, etc. are available without importing in every file (individual tests still import Vitest/APIs where they prefer explicit imports).
- **`environment: "jsdom"`** — DOM APIs for React components.
- **`setupFiles: "./src/test/setup.ts"`** — runs before tests.

### Test files (by area)

| File | What it covers |
| --- | --- |
| `src/components/SearchBar.test.tsx` | Validation, submit, clear, loading/disabled UX |
| `src/components/UserCard.test.tsx` | Profile fields, conditional name/bio/location |
| `src/components/RepoList.test.tsx` | Grid vs empty repos message |
| `src/components/RepoItem.test.tsx` | Repo line, language badge, null description copy |
| `src/hooks/useGithubUser.test.tsx` | Fetch success, 404, errors, network failure (with `fetch` mocked) |
| `src/utils/formatNumber.test.ts` | Number formatting edge cases |

Shared sample data for components lives in **`src/test/mocks.ts`** (`mockUser`, `mockUserMinimal`, `mockRepos`).

### Running tests

```bash
# Interactive watch mode (default when you run `npm test` with no args)
npm test

# Single run (CI-friendly)
npm test -- --run

# One file
npm test -- --run src/components/SearchBar.test.tsx
```

### Coverage

```bash
npm run coverage
```

This produces an **`coverage/`** HTML report (and related artifacts) you can open in a browser (`coverage/index.html`). Consider adding `coverage/` to `.gitignore` if you do not want those files in version control—many teams exclude generated reports.

### Conventions worth following when adding tests

1. Prefer **`getByRole`**, **`getByLabelText`**, and **`getByText`** over brittle CSS selectors—the app uses labels like “GitHub username” and buttons like “Search”.
2. For async UI updates after user actions, use **`waitFor`** or **`findBy*`** queries from Testing Library.
3. When testing **`fetch`**, mock `globalThis.fetch` in the test file so results are deterministic and do not hit the real GitHub API.
4. Keep **mocks** in `src/test/mocks.ts` when multiple specs need the same fixtures.

### End-to-end (E2E) tests

This repository’s **checked-in** automated tests are **unit / component-level** (Vitest + Testing Library). **Browser E2E** (real browser driving the live app) is not part of `npm test` yet—you can add Playwright, Cypress, or similar yourself, or use **TestSprite** below to generate and run broader flows.

### TestSprite (MCP)

[**TestSprite**](https://www.testsprite.com/) provides a **[Model Context Protocol (MCP) server](https://docs.testsprite.com/mcp/getting-started/overview)** that connects tools like **Cursor** to TestSprite’s testing agent. From the IDE you can describe what you want tested in natural language; the agent analyzes the project, can produce normalized requirements and **frontend test plans**, and **generate runnable test code** (e.g. Playwright-style E2E, depending on what the agent selects) with optional **execution and reports**—useful when you want full **user journeys** (search → results → errors) rather than isolated component renders.

**How it relates to this app**

| In repo today | Via TestSprite (when MCP is configured) |
| --- | --- |
| Fast Vitest specs, mocked `fetch`, jsdom | True browser flows against `http://localhost:5173` (or preview) hitting the **real GitHub API** or a stubbed backend, depending on how tests are generated |

**Typical usage with a Vite app like this**

1. Install and enable **TestSprite MCP** in Cursor (follow [TestSprite MCP getting started](https://docs.testsprite.com/mcp/getting-started/overview)).
2. **Run the app** so the MCP tools can reach it—for production-like runs, TestSprite recommends a **built app + static server**, e.g. `npm run build` then `npm run preview`, and aligning the tooling’s **`serverMode`** / port with however you started the server (**5173** is Vite’s default).
3. In chat, use a prompt along the lines of: *“Help me test this project with TestSprite”* or ask specifically for **E2E** coverage of GitHub User Finder (empty state, validation, successful search, 404, Try Again).
4. On **first use**, the agent may create a **`.testsprite/`** (or related) config under the project; follow any on-screen steps in the IDE.

**Environment note**

The TestSprite MCP npm package may declare **`engines.node: ">=22"`**. If you see an **`EBADENGINE`** warning or connection/timeouts, switch the environment Cursor uses to **Node.js 22+**, restart the editor, and retry. Timeouts can also be caused by the app not running, wrong port, or network/proxy issues.

**Docs**

- [TestSprite MCP overview](https://docs.testsprite.com/mcp/getting-started/overview)  
- [MCP demo & examples](https://docs.testsprite.com/learn/mcp-demo)

## Linting

```bash
npm run lint
```

Rules are configured in **`eslint.config.js`** (flat config). Fix reported issues before opening PRs or enable your editor ESLint integration for inline feedback.

## Build output

Production assets are emitted to **`dist/`** after `npm run build`.

## Contributing / learning path

Suggested order when exploring tests:

1. `formatNumber.test.ts` — smallest surface, pure functions  
2. `SearchBar.test.tsx` — controlled form + validation  
3. `useGithubUser.test.tsx` — async state + mocking `fetch`  
4. Composite UI: `RepoList`, `RepoItem`, `UserCard`

---

Originally scaffolded from the Vite React + TypeScript template; adapted into a GitHub User Finder demo with an emphasis on **testing**.
