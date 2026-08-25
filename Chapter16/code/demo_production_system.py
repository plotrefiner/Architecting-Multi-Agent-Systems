from pathlib import Path
import json

from graph_validation import validate_graph_spec
from sql_validation import validate_read_only_sql
from evaluation import path_satisfies_golden

ROOT = Path(__file__).resolve().parents[1]


def main():
    graph = json.loads((ROOT / "artifacts" / "12_graph_spec.json").read_text())
    golden = json.loads((ROOT / "artifacts" / "15_golden_analytics_case.json").read_text())
    sql_candidate = json.loads((ROOT / "artifacts" / "08_sql_candidate.json").read_text())

    print("graph_valid:", validate_graph_spec(graph))
    print("sql_valid:", validate_read_only_sql(sql_candidate["sql"], {"refund_cases"})["validated"])
    print("golden_path_valid:", path_satisfies_golden(golden["expected"]["required_nodes"], golden["expected"]))


if __name__ == "__main__":
    main()
