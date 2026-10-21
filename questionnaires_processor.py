import os
from enum import Enum
from config import QUEST_FILE, FIELDS_NUM, FIELDS_SEPARATOR, FIELD_TYPES, ACCEPTED_FILE, REJECTED_FILE
from name import process_name
from email_address import process_email
from phone_number import process_phone_number
from group import process_group

def verify_file(file_name):
    if not os.path.exists(file_name):
        return False, f"Файл {file_name} не найден"

    return True, file_name

def verify_fields_num(line):
    fields = line.split(FIELDS_SEPARATOR)
    if len(fields) != FIELDS_NUM:
        return False, f"Должно быть {FIELDS_NUM} поля, получено {len(fields)}"

    return True, line

def process_field(field, field_type):
    match field_type:
        case "name":
            answer = process_name(field)
        case "email":
            answer = process_email(field)
        case "phone":
            answer = process_phone_number(field)
        case "group":
            answer = process_group(field)
    
    res = answer["result"]
    data = answer["description"]

    return res, data

def group_by_key(dict_list, key):
    grouped = {}
    for d in dict_list:
        group_key = d[key]
        grouped.setdefault(group_key, []).append(d)
    return grouped

def analyze_result(ok, reject, skip):
    analysis = {"Всего строк в файле": len(ok) + len(reject) + skip,
                "Принято": len(ok), "Отклонено": len(reject),
                "По группам": {}}

    groupped = group_by_key(list(ok.values()), "group")

    for group, records in groupped.items():
        analysis["По группам"][group] = len(records)

    return analysis

def save_results(ok, reject):
    with open(ACCEPTED_FILE, "w", encoding="utf-8") as f:
        for record in ok.values():
            f.write(";".join(list(record.values())) + "\n")

    with open(REJECTED_FILE, "w", encoding="utf-8") as f:
        for record in reject.values():
            f.write(f"{record["data"]}" + f";[{";".join(record["errors"])}]" + "\n")

def read_file():
    res, descr = verify_file(QUEST_FILE)
    if not res:
        return {"result": False, "description": descr}

    reject = {}
    ok = {}
    skipped = 0

    with open(QUEST_FILE, "r", encoding="utf-8") as f:
        record_num = 0
        for line in f:
            record_num += 1
            line = line.rstrip("\n")
            if len(line) == 0:
                skipped += 1
                continue

            res, descr = verify_fields_num(line)
            if not res:
                reject[record_num] = {"data": line, "errors": [descr]}
                continue

            fields = line.split(FIELDS_SEPARATOR)
            is_record_valid = 1
            normalized_fields = []
            errors = []
            for i in range(len(fields)):
                res, data = process_field(fields[i], FIELD_TYPES[i+1])
                is_record_valid *= res
                if res:
                    normalized_fields.append(data)
                else:
                    errors.append(data)

            if is_record_valid:
                ok[record_num] = {"name": normalized_fields[0], "email": normalized_fields[1],
                                  "phone": normalized_fields[2], "group": normalized_fields[3]}
            else:
                reject[record_num] = {"data": line, "errors": errors}

            analysis_res = analyze_result(ok, reject, skipped)
            save_results(ok, reject)

    return {"result": True, "description": {"accepted": ok, "rejected": reject, "analysis": analysis_res}}

            
                



