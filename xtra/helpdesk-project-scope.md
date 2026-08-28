# Helpdesk / Support Ticket System — Project Scope

## 1. Problem statement

Support requests coming through scattered channels (email, calls, WhatsApp) get lost, duplicated, or forgotten. This system turns each request into a **ticket** — a trackable record with an owner and a status — so nothing falls through the cracks and progress is visible to everyone.

## 2. Scope

**This section exists so that we don't build the wrong (unnecessary) things.** Everything below is either explicitly in or explicitly out, so nobody has to guess mid-task. The MVP itself is split in two: **True MVP** (the bare minimum that technically solves the problem) and **Presentable** (what makes it safe to actually demo). "Works if you know exactly what to click" and "works in front of an audience" are different bars — conflating them is how teams either over-build past the deadline or end up showing something embarrassing on defense day.

**True MVP (build this first — the bare functional minimum):**
- Customers can submit a support ticket (subject + description)
- Anyone can view the list of tickets
- Tickets have a status field: `open` → `in-progress` → `closed` (stored and correct; doesn't need to be changeable through the UI yet)
- Layered architecture (Model → Repository → Service → Controller) against MySQL, for the `Ticket` entity

**Presentable (build right after True MVP, before anything else — this is what makes it demoable):**
- Status can actually be changed through the app itself, not just edited in the database
- Basic styling — no unstyled raw HTML forms on defense day
- Basic error handling — invalid input shows a real message, not a blank screen or a raw server error

**In scope, only after Presentable works end-to-end (stretch — build only with time left):**
- User accounts with roles (customer vs agent)
- Agents can be assigned to tickets
- Comments/replies on a ticket
- Priority levels (low/medium/high)

**Out of scope — do not build these, even if there's spare time:**
- Email/SMS notifications
- File attachments on tickets
- Real-time chat
- Anything not named above

If a "good idea" comes up mid-build that isn't on this list: write it down somewhere, don't build it. Revisit after Presentable is done and demoable.

## 3. Roles & responsibilities

| Role | Owns | Deliverables |
|---|---|---|
| **Backend** | `repositories/`, `services/`, `controllers/`, running API, tests for these layers | Working `GET /tickets` and `POST /tickets`, confirmed via `/docs`, with tests written alongside the code (see Section 4) |
| **Database** | ERD, `models/` folder, MySQL setup | `docs/erd.png`, Model matching agreed fields, DB running |
| **Frontend** | UI pages, API calls | Ticket list page + create-ticket form, wired to the real API |

Everyone commits under their own GitHub account and opens pull requests (PRs) for review — see Section 6.

## 4. Milestones (batches) — testing built in, not bolted on

Tests aren't a separate step done at the end. Each batch below expects you to write a small test **before or alongside** the code it covers — that's the actual practice of TDD: write a test that fails, write just enough code to make it pass, move on. "Done" for any piece of code means it runs *and* has a test proving it works, not just that it exists.

| Batch | Goal | Testing expectation | Self-check |
|---|---|---|---|
| **B0 — Setup** | Repo live, stack locked (Python/FastAPI/MySQL), folders scaffolded, everyone can clone & run | — | Can every teammate run the empty app locally? |
| **B1 — True MVP** | `Ticket` end-to-end: create one, list them, on a barebones frontend — completes True MVP (Section 2) | Backend: unit tests for `create_ticket()`, unit tests for `list_tickets()`, written before or right alongside the real function | Does creating a ticket in the UI actually show up on reload? |
| **B2 — Status through the UI** | Status can be changed through the app itself, not just the database — first half of Presentable | unit tests for the status-update Service function, same habit as B1 | Can a ticket move from open → closed through the app, not the database? |
| **B3 — Audit + polish** | Verify the TDD habit actually held up across B1–B2 (no code should exist without a test), plus styling and error handling — completes Presentable | Confirm every Service has a unit test and every Controller has an integration test | Does `pytest` run clean, covering every layer? |
| **B4 — Submission prep** | ERD/UML finalized to match real code, README written, live-defense run-through | — | Can every member explain and modify any layer? |

Stretch items (user roles, agent assignment, comments, priority — Section 2) aren't tied to a fixed batch: the team only starts them if B0–B3 finish with time to spare, and picks them up before B4.

## 5. Per-batch breakdown — who does what

Section 3 says who *owns* which layer overall; this table says what each person is actually doing in each batch, so nobody has to guess where to start on a given day.

| Batch | Backend | Database | Frontend |
|---|---|---|---|
| **B0 — Setup** | Scaffold the FastAPI app (empty `repositories/`, `services/`, `controllers/` folders, a `../main.py` that runs); confirm `uvicorn` boots locally | Install/confirm MySQL running locally; create the empty project database | Scaffold the frontend project; confirm it runs and renders a blank page |
| **B1 — True MVP** | Build Model → Repository → Service → Controller for `create_ticket` and `list_tickets`; write the two required unit tests; confirm both work via `/docs` | Finalize the agreed `Ticket` fields (id, subject, description, status, created_at) and draft the ERD (`docs/erd.png`); create the real MySQL table matching it | Build the barebones ticket list page + create-ticket form, wired to the real API |
| **B2 — Status through the UI** | Add the status-update endpoint + Service function, with its unit test | Confirm the `status` column cleanly supports all three values (migration if needed) | Add a status-change control to the UI (dropdown or buttons), wired to the new endpoint |
| **B3 — Audit + polish** | Fill any missing unit/integration tests found in the audit; add real error handling (validation messages, proper 404s) instead of raw 500s | Verify the live database schema matches the ERD exactly; fix any drift | Basic styling pass; surface backend error messages in the UI instead of a blank failure |
| **B4 — Submission prep** | Write the API section of the README; be ready to explain/modify any layer live | Finalize the ERD/UML to match the shipped code exactly | Write the UI section of the README; be ready to run the live demo |

If B0–B3 finish early, everyone pulls stretch items from Section 2 in Backend/Database/Frontend order of dependency (e.g. the `users` table before the role-check logic before the role-aware UI) — nobody starts a stretch item before B3 is done.