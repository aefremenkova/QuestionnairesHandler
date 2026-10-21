def get_phone_mask(phone):
    digits = [s for s in phone if s.isdigit()]

    mask_phone_parts = ["+7", f"({digits[1:4]})", f"***-**-{digits[9-11]}"]

    return " ".join(mask_phone_parts)

def normalize_phone_number(phone):
    digits = [s for s in phone if s.isdigit()]

    norm_phone_parts = ["+7", f"({"".join(digits[1:4])})", 
                        f"{"".join(digits[4:7])}-{"".join(digits[7:9])}-{"".join(digits[9:])}"]

    return " ".join(norm_phone_parts)

def verify_phone_number(phone):
    digits = [s for s in phone if s.isdigit()]

    if len(digits) != 11:
        return False, f"Номер телефона должен содержать 11 цифр, получено {len(digits)}"

    if digits[0] != "7" and digits[0] != "8":
        return False, f"Номер телефона должен начинаться с 7 или 8, получено {digits[0]}"

    return True, digits

def process_phone_number(phone):
    res, descr = verify_phone_number(phone)
    if not res:
        return {"result": False, "description": descr}

    norm_phone = normalize_phone_number(phone)
    return {"result": True, "description": norm_phone}
