def normalize_name(name):
    norm_parts = [n.capitalize() for n in name.split()]
    norm_name = " ".join(norm_parts)

    return norm_name

def verify_name(name):
    parts = name.split()
    if len(parts) < 2:
        return False, "В ФИО меньше двух слов"

    return True, name

def process_name(name):
    res, descr = verify_name(name)
    if not res:
        return {"result": False, "description": descr}

    norm_name = normalize_name(name)
    return {"result": True, "description": norm_name}
    
