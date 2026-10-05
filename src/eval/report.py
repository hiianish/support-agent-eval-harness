import csv
import statistics
from collections import defaultdict
from datetime import datetime

from src import config


LOWER_IS_BETTER = set()


def label(name):
    return f"{name} (low=good)" if name in LOWER_IS_BETTER else name


def perfect_scores(names):
    return {name: 0.0 if name in LOWER_IS_BETTER else 1.0 for name in names}


def mean(values):
    values = [value for value in values if value is not None]
    return statistics.mean(values) if values else None


def format_value(value):
    return "  n/a" if value is None else f"{value:5.2f}"


def summarize(rows, names):
    groups = defaultdict(list)
    for row in rows:
        groups[row["trap_type"]].append(row)
        groups["ALL"].append(row)
    table = []
    for group in sorted(groups, key=lambda name: (name == "ALL", name)):
        table.append({
            "trap_type": group,
            "n": len(groups[group]),
            **{name: mean([row["scores"].get(name) for row in groups[group]]) for name in names},
        })
    return table


def print_table(table, names, title=None):
    if title:
        print(title)
    header = f"{'trap_type':<16}{'n':>5}" + "".join(f"{label(name):>26}" for name in names)
    print(header)
    print("-" * len(header))
    for line_data in table:
        line = f"{line_data['trap_type']:<16}{line_data['n']:>5}"
        for name in names:
            line += f"{format_value(line_data[name]):>26}"
        print(line)


def new_stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_table(prefix, stamp, table, names, run_info):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    output = config.RESULTS_DIR / f"{prefix}_{stamp}.csv"
    columns = ["run_time", *run_info.keys(), "trap_type", "n", *names]
    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for line_data in table:
            record = {name: "" if line_data[name] is None else round(line_data[name], 4) for name in names}
            writer.writerow({
                "run_time": stamp,
                **run_info,
                "trap_type": line_data["trap_type"],
                "n": line_data["n"],
                **record,
            })
    return output


def save_reasons(prefix, stamp, rows, perfect):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    output = config.RESULTS_DIR / f"{prefix}_{stamp}_reasons.csv"
    columns = ["id", "trap_type", "metric", "score", "question", "answer", "retrieved_docs", "trace", "reason"]
    count = 0
    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            for name, score in row["scores"].items():
                if score is None or abs(score - perfect.get(name, 1.0)) < 1e-9:
                    continue
                writer.writerow({
                    "id": row["id"],
                    "trap_type": row["trap_type"],
                    "metric": name,
                    "score": round(score, 4),
                    "question": row["question"],
                    "answer": row.get("answer", ""),
                    "retrieved_docs": " ".join(row.get("retrieved_doc_ids", [])),
                    "trace": row.get("trace", ""),
                    "reason": row["reasons"].get(name, ""),
                })
                count += 1
    return output, count