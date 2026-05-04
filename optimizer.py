from knapsack import generate_loadout
from backtracker import traverse_dungeon


def optimize_system(all_items, capacity, grid, start, goal):
    mandatory_attrs = set()
    history = []
    iterations = 0
    MAX_ITER = 20

    while iterations < MAX_ITER:
        iterations += 1
        result = generate_loadout(all_items, capacity, mandatory_attrs)
        loadout = result["loadout"]
        loadout_attrs = set(attr for it in loadout for attr in it["attributes"])

        trav = traverse_dungeon(
            grid, tuple(start), tuple(goal), loadout_attrs, record_steps=True
        )

        if trav["success"]:
            history.append({
                "iteration": iterations,
                "loadout": [it["name"] for it in loadout],
                "total_power": result["total_power"],
                "total_weight": result["total_weight"],
                "mandatory_attrs": list(mandatory_attrs),
                "result": "success",
                "missing_attr": None,
                "steps": trav["steps"],
                "path": trav["path"],
                "dp_table": result["dp_table"],
                "dp_capacity": result["capacity_used"]
            })
            return {
                "success": True,
                "solvable": True,
                "loadout": loadout,
                "path": trav["path"],
                "steps": trav["steps"],
                "iterations": iterations,
                "history": history
            }

        missing = trav.get("missing_attr")

        if not missing:
            return {
                "success": False,
                "solvable": False,
                "reason": "No path exists in this dungeon (layout issue)",
                "history": history,
                "iterations": iterations
            }

        pool_has = any(missing in it["attributes"] for it in all_items)
        if not pool_has:
            history.append({
                "iteration": iterations,
                "loadout": [it["name"] for it in loadout],
                "total_power": result["total_power"],
                "total_weight": result["total_weight"],
                "mandatory_attrs": list(mandatory_attrs),
                "result": "blocked",
                "missing_attr": missing,
                "steps": trav["steps"],
                "path": None,
                "dp_table": result["dp_table"],
                "dp_capacity": result["capacity_used"]
            })
            return {
                "success": False,
                "solvable": False,
                "reason": f"No item in pool has attribute: {missing}",
                "history": history,
                "iterations": iterations
            }

        history.append({
            "iteration": iterations,
            "loadout": [it["name"] for it in loadout],
            "total_power": result["total_power"],
            "total_weight": result["total_weight"],
            "mandatory_attrs": list(mandatory_attrs),
            "result": "blocked",
            "missing_attr": missing,
            "steps": trav["steps"],
            "path": None,
            "dp_table": result["dp_table"],
            "dp_capacity": result["capacity_used"]
        })
        mandatory_attrs.add(missing)

    return {
        "success": False,
        "solvable": False,
        "reason": "Max iterations exceeded",
        "history": history,
        "iterations": iterations
    }
