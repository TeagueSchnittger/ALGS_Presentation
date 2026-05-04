# Constraint-Based Loadout & Path Optimizer

A university algorithms presentation tool that visualizes three coupled algorithms in real time: seed-based item generation, 0/1 Knapsack DP, and recursive DFS backtracking — tied together by a feedback loop that resolves gate-key conflicts automatically.

---

## What It Does

1. **Generate** a deterministic item pool from a 64-bit seed
2. **Optimize** a loadout using 0/1 Knapsack DP (maximizing power within a weight capacity)
3. **Traverse** a dungeon grid using recursive DFS backtracking
4. **Feedback loop**: if the DFS hits a locked gate and the loadout lacks the required key attribute, it injects that attribute as mandatory and re-runs the Knapsack — repeating until the dungeon is solved or proven unsolvable

The frontend animates every DFS step live and shows the full iteration history, DP table heatmap, and complexity banner.

---

## File Structure

```
ALGS_Presentation/
├── app.py            # Flask API server + static file serving
├── generator.py      # Seed-based item pool sampling
├── knapsack.py       # Constraint-aware 0/1 Knapsack DP
├── backtracker.py    # Recursive DFS + MissingAttributeException
├── optimizer.py      # Feedback loop orchestrator
├── items.json        # Item database (18 items)
├── dungeons.py       # 3 pre-built dungeon grids
├── requirements.txt  # Python dependencies
└── index.html        # Single-file frontend (vanilla JS)
```

---

## Setup & Installation

### Requirements
- Python 3.8+
- pip

### Install dependencies

```bash
pip install flask flask-cors
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Start the server

```bash
python app.py
```

Server runs on `http://localhost:5000`.

### Open the UI

Navigate to `http://localhost:5000` in your browser.

---

## How to Use

### Controls (left panel)

| Control | Description |
|---------|-------------|
| **Seed** | 64-bit integer — same seed always generates the same item pool |
| **Capacity slider** | Weight limit for the knapsack (10–50) |
| **Dungeon selector** | Choose one of 3 pre-built dungeons |
| **Speed slider** | Animation delay in ms per DFS step (lower = faster) |
| **Run Optimizer** | Runs the full pipeline and animates the result |
| **Step** | Advances animation one DFS move at a time (great for presenting) |
| **Reset** | Clears the grid and history |

### Recommended demo (seed=42, capacity=25, Dungeon 2 — The Gauntlet)

1. Enter seed `42`, set capacity to `25`, select **The Gauntlet**
2. Click **Run Optimizer**
3. Watch iteration 1: DFS explores the maze, hits a fire gate, gets blocked
4. The feedback loop injects `fire_key` as mandatory, re-runs Knapsack
5. Watch iteration 2: DFS hits the ice gate, gets blocked
6. Feedback loop injects `ice_key`, re-runs again
7. Iteration 3: DFS finds a complete path — lights up green

Use **Step** mode to walk through each DFS move one at a time during a live presentation.

---

## Dungeons

| # | Name | Size | Gates | Expected Iterations |
|---|------|------|-------|---------------------|
| 1 | The Tutorial | 5×5 | fire | 2 |
| 2 | The Gauntlet | 8×8 | fire + ice | 3 |
| 3 | The Labyrinth | 10×10 | fire + shadow + arcane | 4 |

All dungeons use `START = (0,0)` (top-left) and `GOAL = bottom-right corner`.

---

## API Endpoints

| Method | Route | Body / Params | Returns |
|--------|-------|---------------|---------|
| `GET` | `/api/dungeons` | — | List of dungeon summaries |
| `GET` | `/api/dungeon/<id>` | — | Full grid, start, goal |
| `POST` | `/api/generate` | `{seed, capacity}` | Item pool |
| `POST` | `/api/optimize` | `{seed, capacity, dungeon_id}` | Full iteration history, steps, DP tables |

---

## Algorithms

### Stage 1 — Item Generation (`generator.py`)
Uses `random.Random(seed).sample(items, n)` to deterministically pick 10 items from the database. Same seed = same pool every time.

### Stage 2 — 0/1 Knapsack DP (`knapsack.py`)
Standard DP recurrence:
```
DP[i][w] = max(DP[i-1][w], power_i + DP[i-1][w - weight_i])
```
Items whose attributes intersect the `required_attrs` set are **hard-locked** into the loadout before DP runs (they bypass the weight check — they're mandatory gate keys).

### Stage 3 — Recursive DFS Backtracker (`backtracker.py`)
Explores Up/Down/Left/Right from start. Uses a `visited` set for O(1) cycle detection. If a `GATE:ATTR` cell is reached and the attribute is missing from the loadout, raises `MissingAttributeException` immediately (prunes that branch).

### Stage 4 — Feedback Loop (`optimizer.py`)
```
mandatory_attrs = {}
loop:
  loadout = knapsack(items, capacity, mandatory_attrs)
  try:
    traverse_dungeon(grid, start, goal, loadout.attrs)
    → success, return
  except MissingAttributeException(attr):
    mandatory_attrs.add(attr)
    → repeat
```

### Complexity
```
O(G · (n·W + 4^k))
```
- **G** = feedback iterations
- **n** = items in pool, **W** = capacity (Knapsack term)
- **k** = cells explored per DFS attempt (backtracker term)

The live complexity banner updates after each iteration.

---

## Item Attributes (Gate Keys)

| Attribute | Gates it unlocks | Color in UI |
|-----------|-----------------|-------------|
| `fire_key` | 🔥 Fire gates | Orange-red |
| `ice_key` | ❄️ Ice gates | Blue |
| `shadow_pass` | 🌑 Shadow gates | Purple |
| `arcane_sigil` | ✨ Arcane gates | Green |

---

## Troubleshooting

**"Server offline" message in UI** — run `python app.py` first, then refresh.

**Port already in use** — kill the existing process or change the port in `app.py` (`port=5001`).

**Dungeon appears unsolvable** — if no item in the generated pool has the required attribute, the API returns `{solvable: false, reason: "..."}`. Try a different seed.

**Animation too fast/slow** — adjust the Speed slider before clicking Run.
