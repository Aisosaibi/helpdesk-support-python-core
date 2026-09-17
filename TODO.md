# Helpdesk Project Todo

This list compares the current frontend workflows with the FastAPI backend. Priorities are ordered by impact.

## P0: Fix Before Demo

- [ ] Fix frontend ticket creation.
  - The frontend must call `POST /tickets/?user_id=<current-user-id>`.
  - Keep `subject`, `description`, `priority`, and `customer_id` in the JSON body.
  - Verify a customer can create a ticket and see it in the ticket list.

- [ ] Add API integration tests for the main workflows.
  - Register a customer.
  - Log in and log out.
  - Create and retrieve a ticket.
  - Add and retrieve a comment.
  - Update status and priority.
  - Assign a ticket to an agent.

- [ ] Update the README with exact startup instructions.
  - `uv sync`
  - `uv run uvicorn app.main:app --reload --port 8000`
  - `cd helpdesk-frontend && python3 -m http.server 5500`
  - Explain `DATABASE_URL` and the SQLite/MySQL options.

## P1: Secure the Application

- [ ] Replace the `is_logged_in` boolean with real authentication.
  - Use signed, expiring access tokens or secure server-side sessions.
  - Send credentials with protected requests.
  - Do not trust user IDs, emails, or roles supplied by the browser.

- [ ] Enforce authorization in backend services/controllers.
  - Customers can access only their own tickets and comments.
  - Agents can work on tickets assigned to them or permitted by policy.
  - Admins can manage users, assignments, and deletion.
  - Apply authorization to list, read, create, update, assign, comment, and delete routes.

- [ ] Lock down registration roles.
  - Public registration must always create a customer.
  - Agent accounts should require an admin workflow or a controlled invite.
  - Do not accept an unrestricted role from a public request.

- [ ] Protect user data.
  - Do not expose password fields or unnecessary user email data.
  - Restrict user update/delete operations to the owner or an admin.
  - Add password validation, email normalization, and login rate limiting.

- [ ] Review CORS and deployment configuration.
  - Use environment-based allowed origins.
  - Require HTTPS and secure cookies/tokens in production.
  - Do not hard-code `http://localhost:8000` in production frontend code.

## P1: Complete Frontend Workflows

- [ ] Make status controls reflect valid transitions.
  - Only offer transitions allowed by the service.
  - Prevent `open -> closed` and other invalid jumps in the UI.
  - Show a useful validation message when the backend rejects a transition.

- [ ] Fix status and priority badge styling for lowercase API values.
  - Support `open`, `in-progress`, `closed` and `low`, `medium`, `high`.

- [ ] Add priority editing to the dashboard.
  - Add a priority control and call `PATCH /tickets/{ticket_id}/priority`.
  - Refresh the ticket details after saving.

- [ ] Improve assignment feedback.
  - Refresh the ticket after assignment.
  - Display the assigned agent in the list and modal.
  - Handle unavailable or deleted agents clearly.

- [ ] Improve comments.
  - Display the comment author name and role.
  - Add loading, empty, retry, and error states.
  - Disable comment submission while a request is in progress.

- [ ] Add dashboard summary metrics.
  - Show open, in-progress, and closed counts for the authenticated user or permitted queue.
  - Avoid exposing operational counts publicly unless that is intentional.

- [ ] Improve request UX.
  - Disable buttons during requests to prevent duplicates.
  - Add Enter/keyboard submission where appropriate.
  - Replace raw JSON error messages with user-friendly messages.
  - Refresh the correct list after delete or update actions.

## P2: Data and Architecture

- [ ] Add database migrations.
  - Use a migration tool such as Alembic.
  - Keep SQLite development schema and MySQL production schema aligned.
  - Stop relying on table creation during module import.

- [ ] Add database constraints and indexes.
  - Unique index for user email.
  - Indexes for ticket status, customer, agent, and creation date.
  - Validate foreign-key relationships for users, tickets, and comments.

- [ ] Add pagination and filtering.
  - Paginate ticket and comment lists.
  - Filter tickets by status, priority, customer, agent, and date.
  - Define stable ordering.

- [ ] Add audit history.
  - Record status changes, assignment changes, deletion, and important user actions.
  - Include actor and timestamp.

- [ ] Decide and document ticket lifecycle rules.
  - Confirm whether closed tickets may be reopened.
  - Define who may change status, priority, and assignment.
  - Keep backend rules and UI controls consistent.

## P2: Testing and Quality

- [ ] Add controller/API tests using FastAPI `TestClient`.
- [ ] Add authorization tests for every protected route.
- [ ] Add tests for invalid status transitions and invalid roles.
- [ ] Add tests for ticket ownership and comment ownership.
- [ ] Add tests for duplicate email, malformed input, missing users, and missing tickets.
- [ ] Add frontend browser tests for login, ticket creation, comments, assignment, and status updates.
- [ ] Add a smoke test that starts both servers and checks the browser flow.
- [ ] Add formatting/linting/type-checking commands to the project workflow.

## P3: Documentation and Operations

- [ ] Reconcile `xtra/helpdesk-project-scope.md` with the actual project.
  - It currently says the frontend is out of scope, but a frontend now exists.

- [ ] Document the API contract.
  - Request and response examples.
  - Authentication requirements.
  - Role permissions.
  - Error response format.

- [ ] Add environment configuration examples.
  - Provide `.env.example` without secrets.
  - Document SQLite development and MySQL deployment settings.

- [ ] Add production deployment guidance.
  - Process manager/container setup.
  - Static frontend hosting.
  - Database backup and migration procedure.
  - Logging and health checks.

## Already Working

- [x] FastAPI app starts with local SQLite by default.
- [x] Customer registration and login service behavior.
- [x] Ticket, comment, user, and priority service tests.
- [x] Frontend static server workflow.
- [x] Frontend/backend route contract alignment for most ticket and comment operations.
- [x] Landing-page ticket summary endpoint and database-backed counts.
- [x] Blue-green frontend theme.
