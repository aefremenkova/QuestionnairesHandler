def group_by_key(dict_list, key):
    grouped = {}
    for d in dict_list:
        group_key = d[key]
        grouped.setdefault(group_key, []).append(d)
    return grouped

def get_phone_mask(phone):
    digits = [s for s in phone if s.isdigit()]

    mask_phone_parts = ["+7", f"({digits[1:4]})", f"***-**-{digits[9-11]}"]

    return " ".join(mask_phone_parts)
