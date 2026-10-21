def normalize_group(group):
    return group.replace(" ", "").lower()

def verify_group(group):
    group = group.strip()
    if len(group) == 0:
        return False, "Пустой номер группы"

    return True, group

def process_group(group):
    res, descr = verify_group(group)
    if not res:
        return {"result": False, "description": descr}

    norm_group = normalize_group(group)
    return {"result": True, "description": norm_group}
