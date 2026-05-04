class MissingAttributeException(Exception):
    def __init__(self, attr):
        self.attr = attr
        super().__init__(f"Missing attribute: {attr}")


def traverse_dungeon(grid, start, goal, loadout_attrs, visited=None, record_steps=False):
    if visited is None:
        visited = set()
    steps = []
    path_stack = []
    found_missing = [None]

    def dfs(pos):
        r, c = pos
        if pos in visited:
            return False
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return False

        cell = grid[r][c]
        if cell == 1:
            return False

        if isinstance(cell, str) and cell.startswith("GATE:"):
            attr = cell.split(":", 1)[1]
            if attr not in loadout_attrs:
                # record the blocked gate as a visit so animation shows it
                if record_steps:
                    steps.append(("blocked", r, c))
                if found_missing[0] is None:
                    found_missing[0] = attr
                return False

        visited.add(pos)
        path_stack.append(pos)
        if record_steps:
            steps.append(("visit", r, c))

        if pos == goal:
            return True

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            npos = (r + dr, c + dc)
            if dfs(npos):
                return True

        path_stack.pop()
        if record_steps:
            steps.append(("backtrack", r, c))
        return False

    success = dfs(start)

    path = None
    if success:
        path = [[r, c] for r, c in path_stack]

    result = {
        "success": success,
        "missing_attr": found_missing[0],
        "steps": steps if record_steps else [],
        "path": path
    }

    if not success and found_missing[0] is None and not result["missing_attr"]:
        result["no_path"] = True

    return result
