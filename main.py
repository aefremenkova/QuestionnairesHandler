from questionnaires_processor import read_file
from config import ACCEPTED_FILE, REJECTED_FILE
from report import print_accepted_questionnaires, print_rejected_questionnaires, analyze_result
from storage import save_results

def main():
    res = read_file()
    if res["result"]:
        print_accepted_questionnaires(res["description"]["accepted"])
        print_rejected_questionnaires(res["description"]["rejected"])
        analyze_result(res["description"])
        save_results(res["description"]["accepted"], res["description"]["rejected"])
        print(f"Принятые анкеты сохранены в файле {ACCEPTED_FILE}, отклонённые - в {REJECTED_FILE}")
    else:
        print(res["description"])


if __name__ == "__main__":
    main()
