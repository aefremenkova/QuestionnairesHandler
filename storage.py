from config import ACCEPTED_FILE, REJECTED_FILE

def save_results(ok, reject):
    with open(ACCEPTED_FILE, "a", encoding="utf-8") as f:
        for record in ok.values():
            f.write(";".join(list(record.values())) + "\n")

    with open(REJECTED_FILE, "a", encoding="utf-8") as f:
        for record in reject.values():
            f.write(f"{record["data"]}" + f";[{";".join(record["errors"])}]" + "\n")

def read_file(file):
    records = []
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            records.append(line)

    return records