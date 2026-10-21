from questionnaires_processor import read_file
from utils import get_phone_mask, find_cols_width
from config import ACCEPTED_FILE, REJECTED_FILE

COL_HEADER_KEY = {"№": None, "ФИО": "name", "Эл.адрес": "email", 
                  "Телефон": "phone", "Группа": "group"}

def print_accepted_questionnaires(quest_dict):
    cols_width = find_cols_width(quest_dict, COL_HEADER_KEY)
    headers = []
    for k, v in cols_width.items():
        headers.append(f"{k:<{v}}")
    headers = "".join(headers)

    sorted_dict = dict(sorted(quest_dict.items(), key=lambda item: item[1]['name']))
    i = 1
    
    print(headers)
    print("-" * len(headers))
    for v in sorted_dict.values():
        masked_phone = get_phone_mask(v["phone"])
        record = []
        for header, key in COL_HEADER_KEY.items():
            if key is None:
                record.append(f"{i:<{cols_width[header]}}")
            elif key == "phone":
                record.append(f"{masked_phone:<{cols_width[header]}}")
            else:
                record.append(f"{v[key]:<{cols_width[header]}}")
        print("".join(record))
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
