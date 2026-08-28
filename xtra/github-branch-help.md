# GitHub — for everyone, zero assumed experience

## First: why do we even need "branches"? (the problem this solves)

Picture the team working *without* branches — everyone editing the same files on `main` at once. Sade adds a field to the `Ticket` model at 2pm. At the same time, Ade is halfway through wiring the API, and his code assumes the model *without* Sade's field. He pushes. Now `main` is broken, nobody knows whose change did it, and if a teammate pulls at 2:05pm, they inherit a codebase that doesn't run — through no fault of their own.

A **branch** is GitHub's fix for that: it's your own private, full copy of the codebase to edit in, that doesn't touch `main` until you say so. Sade works on her branch, Ade works on his — neither can break the other's copy — and `main` only changes in deliberate, reviewed steps. That's the entire reason the workflow below exists: not process for its own sake, but "how do 3 people edit the same project without stepping on each other."

## The five words you need

- **Repo** — the project's shared home on GitHub. Ours: `helpdesk-support-system`.
- **Branch** — your own private lane to make changes in, without touching the official version yet.
- **Commit** — a saved checkpoint of your changes, with a short message describing what changed.
- **Push** — sending your commits from your computer up to GitHub.
- **Pull Request (PR)** — a request: "here's my branch, please review and merge it into `main`."

## The shape of it

```
Your computer                        GitHub
--------------                       -----------------------------------
edit files, commit  --- push --->    your branch (feature/ticket-api)
                                              |
                                      open a Pull Request
                                              |
                                      a teammate reviews it
                                              |
                                              v
                                            main   <- always kept working
```

`main` never gets touched directly by anyone. That's the whole rule.

## A full worked example — Sade builds the Ticket model

This is the exact sequence, start to finish, for one piece of work. Everyone on the team runs this same sequence for their own tasks, just with different branch names and commit messages.

**Step 1 — Start from an up-to-date `main`, then branch off it. For example:**
```bash
git checkout main
git pull
git checkout -b feature/ticket-model
```
`checkout -b` does two things at once: creates the new branch, and switches you onto it. From this point, anything Sade edits only exists on `feature/ticket-model` — `main` is untouched.

Example branch names for this project: `feature/ticket-model`, `feature/ticket-api`, `feature/ticket-frontend`, `feature/erd`.

**Step 2 — Edit files normally, then save a checkpoint:**
```bash
git add .
git commit -m "Add Ticket model with subject, description, status fields"
```
`git add .` stages every changed file; `git commit` saves that snapshot locally, on Sade's laptop only — nothing has left her computer yet. Commit messages should say *what changed*, in plain words — a teammate should understand it without opening the file. Small, frequent commits (one per logical change) are easier to review and undo than one giant commit at the end.

**Step 3 — Send the branch to GitHub:**
```bash
git push -u origin feature/ticket-model
```
`-u` only needed the very first push of that branch; after that, plain `git push` works. This is the moment Sade's work becomes visible to the rest of the team — but it's still sitting on her branch, not on `main`.

**Step 4 — Open the Pull Request:** go to the repo on GitHub — it'll show a yellow banner "Compare & pull request" for the just-pushed branch. Click it, write a one-line description of what the PR does, and open it. This is Sade formally asking: "please review this before it becomes part of the real project."

**Step 5 — Get it reviewed and merged:** a teammate opens the PR, reads the changes, comments if something looks off, then clicks "Merge" once it's good. Now Sade's model is part of `main`, and everyone else can pull it in.

**Step 6 — Before starting the *next* task, sync `main` again:**
```bash
git checkout main
git pull
```
This pulls in everyone else's merged work before branching off again — including anything that got merged while Sade was working — so nobody ever builds on stale code. Then repeat from Step 1 for the next task.

## QAs

- **"What if I forget to branch and just start editing on `main`?"** Stop, run `git status` to confirm what's changed, then `git stash`, `git checkout -b feature/whatever`, `git stash pop` — this moves your uncommitted edits onto a fresh branch without losing them. Easier: just remember to `git checkout -b ...` *before* opening your editor.
- **"Do I need permission to make a branch?"** No — branches are free and local-first; you can make and delete as many as you like. Only merging into `main` needs a teammate's review.
- **"What happens to my branch after it's merged?"** Nothing bad — it just sits there, unused. You can delete it on GitHub (there's a button right after merging) or leave it; either is fine.
- **"What's a merge conflict?"** It happens when two people's *committed* changes touch the exact same lines. GitHub will tell you exactly which lines and ask you to pick (or combine) the versions — it won't happen silently, and it won't happen at all if everyone keeps branches short-lived and pulls `main` often.
- **"I pushed but don't see the yellow banner — now what?"** Go to the repo's GitHub page directly, click "Pull requests" → "New pull request", and pick your branch manually from the dropdown. Same result, just one extra click.