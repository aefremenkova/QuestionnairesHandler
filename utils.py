def group_by_key(dict_list, key):
    grouped = {}
    for d in dict_list:
        group_key = d[key]
        grouped.setdefault(group_key, []).append(d)
    return grouped

def get_phone_mask(phone):
    digits = [s for s in phone if s.isdigit()]

    mask_phone_parts = ["+7", f"({"".join(digits[1:4])})", f"***-**-{"".join(digits[9:])}"]

    return " ".join(mask_phone_parts)

def find_cols_width(quest_dict, header_key_conn):
    cols_width = {}
    correction = 3

    for header, key in header_key_conn.items():
        if key is None:
            cols_width[header] = len(quest_dict) + correction
        else:
            cols_width[header] = max(len(val) for val in [v.get(key, None) for v in list(quest_dict.values())]) + correction

    return cols_width