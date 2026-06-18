# Nornir Foundations: Inventory, Connections & First Tasks

> **Level:** Basic · **Project 1 of 6** in the Nornir Learning Track
> The "hello world" of Nornir. By the end you'll understand *how Nornir thinks* — and
> everything in projects 2–6 builds directly on this.

---

## What you'll be able to do
Connect to multiple network devices at once, run a read-only command across all of them in
parallel, and read back a clean, structured result — without writing a single per-device loop
by hand.

## Why this matters
Most beginners try to learn Nornir by copying a config-push script. That skips the one thing
that actually makes Nornir powerful: it separates **inventory** (what your devices are),
**tasks** (what you want to do), and the **runner** (how it executes, in parallel). Get this
mental model right once and every later project is just a new task plugged into the same engine.

## Prerequisites
- Comfortable with Python basics (functions, dictionaries, imports).
- A small lab you control — EVE-NG with 3–4 devices is ideal (mix vendors if you can).
- SSH reachability and known credentials to those devices.

## Core concepts you'll learn
- **The three-file inventory:** `hosts`, `groups`, `defaults`, and how values *inherit*
  (a host takes its platform/credentials from its group, and the group from defaults).
- **`config.yaml`:** how Nornir is told where its inventory lives and how many workers run at once.
- **Initialising Nornir:** turning that config into a live object you can run tasks against.
- **Filtering:** selecting a subset of the inventory (one site, one role, one platform).
- **Tasks:** a unit of work Nornir runs once per host.
- **The result hierarchy:** `AggregatedResult` (all hosts) → `MultiResult` (one host's task chain)
  → `Result` (a single task's output). This is how you read success, failure, and output.

## Suggested project layout (described, no code)
```
nornir-learning/
├── config.yaml            # points Nornir at the inventory + sets worker count
├── inventory/
│   ├── hosts.yaml         # each device + which group it belongs to
│   ├── groups.yaml        # shared platform/credentials/port per device type
│   └── defaults.yaml      # fallback values used when not set elsewhere
├── 01_nornir-getting-started/
│   ├── runner.py          # init Nornir, filter, run the task, print results
│   └── README.md
└── README.md
```

## Step-by-step (the logic — you write the code)

**Step 1 — Build the topology first.**
Stand up your lab devices and confirm you can SSH to each one manually. Automation can't reach
what you can't reach by hand. Note each device's IP, platform, and credentials.

**Step 2 — Model the inventory with inheritance in mind.**
Put the *shared* values (platform, username, password, port) in `groups.yaml`, one group per
device type. In `hosts.yaml`, each device only carries what's unique to it (its name, its IP,
the group it belongs to). Anything still missing falls back to `defaults.yaml`. The discipline:
**never repeat a value** — push it up to the most general place it's true.

**Step 3 — Write `config.yaml`.**
Tell Nornir which inventory plugin to use and where the three files are, and set how many hosts
to work on simultaneously (the worker count). Start small while testing.

**Step 4 — Initialise and inspect.**
In the runner, initialise Nornir from `config.yaml`. Before running anything, print the loaded
inventory and confirm every host appears with the *correct inherited values*. This single check
catches 80% of beginner inventory mistakes.

**Step 5 — Apply a filter.**
Select a subset — e.g. only one platform, or one site. Confirm the filtered set contains exactly
who you expect. Filtering is how every real job is scoped, so practise it now.

**Step 6 — Run one read-only task.**
Dispatch a single "show" style command (something harmless like show version / show clock)
across the filtered hosts. Nornir runs them in parallel automatically — you do not loop.

**Step 7 — Read the result properly.**
Walk the result object: iterate hosts, check whether each host's task failed, and print its
output. Deliberately break one host (wrong IP or password) and observe how Nornir reports a
*partial* failure — the rest still succeed. Understanding this now saves you in later projects.

## What "done" looks like
- Running `runner.py` connects to all your lab devices at once and prints each one's output.
- A single broken device shows a clear failure for that host only; others still return output.
- You can explain, out loud, what `AggregatedResult`, `MultiResult`, and `Result` each represent.

## Stretch goals
- Add a second group for a different vendor and confirm inheritance still resolves correctly.
- Increase the worker count and observe the speed difference on a parallel run.
- Filter by a custom attribute you invent (e.g. a `tier` field) to prove filtering is data-driven.

## Interview value
This is where you can confidently explain Nornir's architecture: pure-Python (no DSL), inventory
inheritance, native concurrency, and the result model. Being able to draw the inventory → task →
runner flow on a whiteboard signals you actually *use* the tool, not just quote it.