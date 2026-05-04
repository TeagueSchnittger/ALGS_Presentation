# All dungeons use START=(0,0), GOAL=bottom-right corner.
# Gates sit on the ONLY path to the goal — no bypass routes.
#
# Dungeon 1 (5x5) snake path:
#   Row 0 → right → (0,4) → col 4 down → (1,4) → row 2 left → (2,0) → col 0 down → (3,0)
#   → row 4 right → FIRE GATE at (4,2) → goal (4,4)
#
# Dungeon 2 (8x8) snake path:
#   Row 0 → right → (0,7) → col 7 down → (2,7) → row 3 left → FIRE GATE (3,1) → col 1 down
#   → (5,1) → row 6 right → (6,6) → ICE GATE (7,6) → goal (7,7)
#
# Dungeon 3 (10x10) snake path:
#   Row 0 right → col 9 down → FIRE GATE (2,8) → row 2 left → col 0 down → row 4 right
#   → col 8 down → SHADOW GATE (6,1) → col 1 down → row 8 right → ARCANE GATE (8,8) → goal (9,9)

DUNGEONS = {
    1: {
        "id": 1,
        "name": "The Tutorial",
        "description": "5×5 — one fire gate on the only path to the goal",
        "start": [0, 0],
        "goal": [4, 4],
        "grid": [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, "GATE:fire_key", 0, 0]
        ]
        # Path: (0,0)→(0,4)→(1,4)→(2,4)→(2,3)→(2,2)→(2,1)→(2,0)→(3,0)→(4,0)→(4,1)→FIRE→(4,3)→(4,4)
    },
    2: {
        "id": 2,
        "name": "The Gauntlet",
        "description": "8×8 — fire gate then ice gate, no bypass",
        "start": [0, 0],
        "goal": [7, 7],
        "grid": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, "GATE:fire_key", 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, "GATE:ice_key", 0]
        ]
        # Path: (0,0)→(0,7)→(1,7)→(2,7)→(3,7)→…→FIRE(3,1)→(4,1)→(5,1)→(6,1)→…→(6,6)→ICE(7,6)→(7,7)
    },
    3: {
        "id": 3,
        "name": "The Labyrinth",
        "description": "10×10 — fire, shadow, and arcane gates, no bypass",
        "start": [0, 0],
        "goal": [9, 9],
        "grid": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, "GATE:fire_key", 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, "GATE:shadow_pass", 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, "GATE:arcane_sigil", 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
        ]
        # Path: (0,0)→(0,9)→(1,9)→(2,9)→FIRE(2,8)→(2,0)→(3,0)→(4,0)→…→(4,8)→(5,8)
        #       →(6,8)→…→SHADOW(6,1)→(7,1)→(8,1)→…→ARCANE(8,8)→(9,8)→(9,9)
    }
}
