def generate_loadout(items: list, capacity: int, required_attrs: set) -> dict:
    locked = [it for it in items if set(it["attributes"]) & required_attrs]
    free = [it for it in items if it not in locked]

    locked_weight = sum(it["weight"] for it in locked)
    locked_power = sum(it["power"] for it in locked)
    remaining_cap = capacity - locked_weight

    n = len(free)
    W = max(remaining_cap, 0)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i, item in enumerate(free, 1):
        w, p = item["weight"], item["power"]
        for cap in range(W + 1):
            dp[i][cap] = dp[i-1][cap]
            if w <= cap:
                dp[i][cap] = max(dp[i][cap], p + dp[i-1][cap - w])

    # Reconstruct
    selected = []
    cap = W
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i-1][cap]:
            selected.append(free[i-1])
            cap -= free[i-1]["weight"]

    full_loadout = locked + selected
    return {
        "loadout": full_loadout,
        "locked": locked,
        "selected": selected,
        "total_power": locked_power + dp[n][W],
        "total_weight": locked_weight + sum(it["weight"] for it in selected),
        "dp_table": dp,
        "capacity_used": W
    }
