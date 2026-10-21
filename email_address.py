def normalize_email(email):
    return email.lower()

def verify_email(email):
    errors = []

    at_count = email.count("@")
    if at_count != 1:
        return False, "В эл.адресе отсутствует @" if at_count == 0 else "В эл.адресе несколько @"
    
    parts = email.split("@")
    if any(p == '' for p in parts):
        return False, "Пустое имя почтового ящика или домен в эл.адресе"

    user = parts[0]
    domen = parts[1]

    if "." not in domen:
        errors.append("В домене эл.адреса отсутствует точка")

    if domen[0] == ".":
        errors.append("В домене эл.адреса отсутствует имя домена")

    if domen[-1] == ".":
        errors.append("В домене эл.адреса отсутствует доменная зона")

    if len(errors) != 0:
        return False, errors

    return True, email

def process_email(email):
    res, descr = verify_email(email)
    if not res:
        return {"result": False, "description": descr}

    norm_email = normalize_email(email)
    return {"result": True, "description": norm_email}