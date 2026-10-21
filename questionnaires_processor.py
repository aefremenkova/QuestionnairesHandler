import os
from enum import Enum
from config import QUEST_FILE, FIELDS_NUM, FIELDS_SEPARATOR, FIELD_TYPES
from name import process_name
from email_address import process_email
from phone_number import process_phone_number
from group import process_group
from utils import group_by_key
from storage import read_file

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

def process_records():
    res, descr = verify_file(QUEST_FILE)
    if not res:
        return {"result": False, "description": descr}

    reject = {}
    ok = {}
    skipped = 0

    records = read_file()
    for i in range(len(records)):
        record_num = i + 1
        line = records[i].rstrip("\n")

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

    return {"result": True, "description": {"accepted": ok, "rejected": reject, "skipped": skipped}}

            
                



