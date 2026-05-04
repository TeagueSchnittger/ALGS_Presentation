# CLAUDE.md — Constraint-Based Loadout Selection & Path Optimizer

## Project Overview

Build a full-stack demo application for a university algorithms project. The backend implements
three coupled algorithms; the frontend visualizes each stage live so it can be used as a
presentation tool. The core novelty is a **cross-algorithm dependency feedback loop** that ties
a 0/1 Knapsack DP engine to a recursive backtracking dungeon pathfinder.

---

## Tech Stack

- **Backend:** Python 3 (no heavy frameworks; Flask for the API server is fine)
- **Frontend:** Single HTML file with vanilla JS + CSS (or a single React/JSX file if preferred)
- **Data:** JSON flat-file as the item database (`items.json`)
- **No external DB required** — everything lives in memory or flat files

---

## Core Architecture (3 Stages + Feedback Loop)

### Stage 1 — Deterministic Item Generation (`generator.py`)
- Accept a **64-bit integer seed** (e.g. `12345678901234`)
- Use Python's `random.seed(seed)` to deterministically sample **N items** (e.g. 8–12) from the
  full item database (`items.json`)
- Return the sampled item pool — same seed always yields the same pool

### Stage 2 — Constraint-Aware 0/1 Knapsack (`knapsack.py`)
Implement the standard DP recurrence:
```
DP[i][w] = max(DP[i-1][w], power_i + DP[i-1][w - weight_i])
```
- **`generate_loadout(items, capacity, required_attrs)`**
  - Pre-filter: any item whose attributes intersect `required_attrs` is **hard-locked** into the
    loadout (bypasses the weight check — these are mandatory gate keys)
  - Run 0/1 Knapsack DP on the remaining items with `capacity` reduced by locked items' weight
  - Reconstruct and return the full loadout (locked items + DP-selected items)
- Return: selected item list + total power + total weight + the full DP table (for visualization)

### Stage 3 — Recursive Backtracker (`backtracker.py`)
- **`traverse_dungeon(grid, start, goal, loadout_attrs, visited=None)`**
- Grid cell values:
  - `0` = open path
  - `1` = wall (impassable)
  - `"GATE:ATTR_NAME"` = requires attribute `ATTR_NAME` in loadout
- DFS exploring Up/Down/Left/Right neighbors
- Use a `visited` set for O(1) cycle detection
- If a Gate cell is reached and the required attribute is **missing**, raise a custom
  `MissingAttributeException(missing_attr)` immediately (prune that path)
- Return `(success: bool, path: list[tuple] | None)`

### Stage 4 — Feedback Loop Orchestrator (`optimizer.py`)
- **`optimize_system(all_items, capacity, grid, start, goal)`**
- `mandatory_attrs = set()`
- Loop:
  1. Call `generate_loadout(all_items, capacity, mandatory_attrs)`
  2. Extract all attribute strings from the loadout into a set
  3. Try `traverse_dungeon(grid, start, goal, loadout_attrs)`
  4. On `MissingAttributeException`: add missing attr to `mandatory_attrs`, repeat
  5. On success: return `{loadout, path, iterations, history}`
  6. If `capacity` is exceeded by mandatory items: return failure state
- **Track history per iteration** (for animation): each loop records the loadout tried,
  missing attr found, and traversal attempt

---

## Item Database (`items.json`)

Create a file with **at least 15 items**. Each item:
```json
{
  "id": 1,
  "name": "Iron Sword",
  "weight": 4,
  "power": 10,
  "attributes": []
}
```

Include a variety:
- **Pure power items** (high power, moderate weight, no attributes): swords, armor, rings
- **Utility/key items** (lower power, light weight, critical attributes):
  - `"fire_key"` — unlocks fire gates
  - `"ice_key"` — unlocks ice gates  
  - `"shadow_pass"` — unlocks shadow gates
  - `"arcane_sigil"` — unlocks arcane gates
- **Hybrid items** (moderate power + one attribute)
- Make sure the optimal pure-power loadout intentionally lacks some gate keys (this is the
  "Utility vs. Power gap" that the feedback loop resolves)

---

## Flask API (`app.py`)

Endpoints:

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/api/generate` | Body: `{seed, capacity}` → returns item pool |
| `POST` | `/api/optimize` | Body: `{seed, capacity, dungeon_id}` → runs full pipeline, returns iteration history |
| `GET`  | `/api/dungeons` | Returns list of available pre-built dungeons |
| `GET`  | `/api/dungeon/<id>` | Returns full grid + start + goal for a dungeon |

All responses are JSON. Include CORS headers for local development.

---

## Pre-Built Dungeons (`dungeons.py` or `dungeons.json`)

Provide **3 dungeons** of increasing complexity:

**Dungeon 1 — "The Tutorial"** (5×5)
- One fire gate blocking the only path to goal
- The optimal power loadout will lack `fire_key`, triggering exactly 1 feedback iteration

**Dungeon 2 — "The Gauntlet"** (8×8)
- Two gates (`fire_key`, `ice_key`) on different branches
- Maze-like walls forcing real DFS exploration
- Optimal power loadout lacks both keys, triggering 2 iterations

**Dungeon 3 — "The Labyrinth"** (10×10)
- Three gates (`fire_key`, `shadow_pass`, `arcane_sigil`)
- Multiple dead ends
- Designed to demonstrate G=3 feedback iterations

Use `START = (0, 0)` and `GOAL = bottom-right corner` for all dungeons.

---

## Frontend Visualization (`index.html`)

A single-page presentation tool with three panels:

### Panel 1 — Controls
- Seed input (number field, default `42`)
- Capacity slider (range 10–50, default 25)
- Dungeon selector (dropdown with the 3 pre-built dungeons)
- **"Run Optimizer"** button
- Show current iteration counter while running

### Panel 2 — Dungeon Grid (center, largest panel)
- Render the dungeon as a colored grid:
  - ⬜ White = open path
  - ⬛ Dark = wall
  - 🔴/🟠/🟣 Colored = gate (color per attribute type)
  - 🟢 Green = start
  - ⭐ Gold = goal
  - 🔵 Blue = current DFS path being explored (animated)
  - ✅ Bright green = final successful path
- Animate the backtracker step-by-step (configurable speed slider)
- Show gate labels (e.g. "🔥 Fire Gate")

### Panel 3 — Iteration History (right sidebar)
For each feedback loop iteration, show a card:
- **Iteration #**
- Loadout selected (item names, total power, total weight)
- Result: ✅ Success or ❌ Blocked by `[attribute]`
- Which attribute was injected as mandatory for the next round

Below the history, show a **DP Table visualization** for the current iteration:
- Render the n×W table as a small heatmap or color-graded grid
- Highlight cells that changed from the previous iteration

### Visual Style
- Dark theme (dungeon aesthetic): dark background, bright accent colors
- Use a monospace or slightly stylized font
- Keep it clean — this is a CS presentation, not a game

---

## Complexity Display

Somewhere on the page, show a live-updating complexity banner:
```
Current Complexity: O(G · (n·W + 4^k))
G = [iterations so far]   n = [items in pool]   W = [capacity]   k = [cells explored]
```

Update the values after each iteration completes.

---

## File Structure

```
project/
├── app.py              # Flask server + routes
├── generator.py        # Seed-based item pool generation
├── knapsack.py         # Constraint-aware 0/1 Knapsack DP
├── backtracker.py      # Recursive DFS backtracker + MissingAttributeException
├── optimizer.py        # Feedback loop orchestrator
├── items.json          # Item database (15+ items)
├── dungeons.py         # Pre-built dungeon definitions
├── requirements.txt    # flask, flask-cors (minimal)
└── index.html          # Single-file frontend
```

---

## Implementation Notes

1. **History for animation**: The optimizer must record every DFS step (not just the result)
   so the frontend can replay the traversal. Add an optional `record_steps=True` parameter
   to `traverse_dungeon` that appends each visited cell to a steps log.

2. **DP table serialization**: Return the DP table as a 2D list of ints in the API response
   so the frontend can render it.

3. **Determinism**: With the same seed + same dungeon, the output must always be identical.
   Document the seed in the UI so it can be shared.

4. **Error handling**: If the item pool generated from the seed has no item with a required
   attribute (i.e., the dungeon is unsolvable with this seed), return a clear error state
   `{solvable: false, reason: "No item in pool has attribute: shadow_pass"}`.

5. **Step-through mode**: Add a "Step" button alongside "Run" that advances the animation
   one DFS move at a time — useful for presenting the algorithm in class.

---

## What "Done" Looks Like

- `python app.py` starts the server on `localhost:5000`
- Opening `index.html` (or `localhost:5000`) shows the full UI
- Entering seed `42`, capacity `25`, selecting "The Gauntlet" and clicking Run:
  - Shows the item pool generated
  - Animates the first DFS attempt getting blocked at a gate
  - Shows the feedback loop injecting a mandatory attribute
  - Re-runs Knapsack with the constraint, shows updated loadout
  - Animates the second (successful or partially successful) traversal
  - Final successful path lights up in green
- The complexity banner updates live throughout
