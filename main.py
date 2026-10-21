from questionnaires_processor import read_file
from phone_number import get_phone_mask
from config import ACCEPTED_FILE, REJECTED_FILE

def find_cols_width(quest_dict):
    cols_width = {}

    cols_width["№"] = len(quest_dict) + 3
    cols_width["ФИО"] = max(len(name) for name in [v.get("name", None) for v in list(quest_dict.values())]) + 3
    cols_width["Email"] = max(len(email) for email in [v.get("email", None) for v in list(quest_dict.values())]) + 3
    cols_width["Телефон"] = max(len(phone) for phone in [v.get("phone", None) for v in list(quest_dict.values())]) + 3
    cols_width["Группа"] = max(len(group) for group in [v.get("group", None) for v in list(quest_dict.values())]) + 3

    return cols_width

def print_accepted_questionnaires(quest_dict):
    cols_width = find_cols_width(quest_dict)
    headers = []
    for k, v in cols_width.items():
        headers.append(f"{k:<{v}}")
    headers = "".join(headers)

    sorted_dict = dict(sorted(quest_dict.items(), key=lambda item: item[1]['name']))
    i = 1
    
    print(headers)
    print("-" * len(headers))
    for v in sorted_dict.values():
        masked_phone = v["phone"]
        print(f"{i:<{cols_width["№"]}}{v["name"]:<{cols_width["ФИО"]}}{v["email"]:<{cols_width["Email"]}}" +
        f"{masked_phone:<{cols_width["Телефон"]}}{v["group"]:<{cols_width["Группа"]}}")
        i += 1
    print("-" * len(headers))
    print("\n")

def print_rejected_questionnaires(quest_dict):
    print(f"Отклонено строк: {len(quest_dict)}")
    for k, v in quest_dict.items():
        print(f"\t строка {k}: {";".join(v["errors"])}")
        print(f"\t\t{v["data"]}")
    print("\n")

def print_analysis_res(res_dict):
    for k, v in res_dict.items():
        if type(v) != dict:
            print(f"{k}: {v}")
        else:
            print(f"{k}:")
            for k2, v2 in v.items():
                print(f"\t{k2}: {v2}")
    print("\n")

def main():
    res = read_file()
    if res["result"]:
        print_accepted_questionnaires(res["description"]["accepted"])
        print_rejected_questionnaires(res["description"]["rejected"])
        print_analysis_res(res["description"]["analysis"])
        print(f"Принятые анкеты сохранены в файле {ACCEPTED_FILE}, отклонённые - в {REJECTED_FILE}")
    else:
        print(res["description"])


if __name__ == "__main__":
    main()
