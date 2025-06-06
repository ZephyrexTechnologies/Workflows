import json
import pathlib
from collections import defaultdict
import sys


def main():
    pull_request_dict = defaultdict(list)
    destination_branch_dict = defaultdict(list)
    pull_request_fp = pathlib.Path(sys.argv[1])
    destination_branch_fp = pathlib.Path(sys.argv[2])
    with open(pull_request_fp, "r") as f:
        pull_request_results = f.read().splitlines()[3:-1]  # Trim unnecessary entries
        for item in pull_request_results:
            print(f"ITEM: {item}")
            json_data = json.loads(item)
            if "nodeid" in json_data.keys():
                pull_request_dict[json_data["outcome"]].append(json_data["nodeid"])
    with open(destination_branch_fp, "r") as f:
        destination_branch_results = f.read().splitlines()[
            3:-1
        ]  # Trim unnecessary entries
        for item in destination_branch_results:
            json_data = json.loads(item)
            if "nodeid" in json_data.keys():
                destination_branch_dict[json_data["outcome"]].append(
                    json_data["nodeid"]
                )
    regressions = []
    warnings = []
    for item in destination_branch_dict["passed"]:
        if item in pull_request_dict["failed"]:
            regressions.append(item)
        elif item in pull_request_dict["skipped"]:
            warnings.append(item)
    print(f"{len(warnings)} tests now skipped/xfailed that weren't previously")
    for warning in warnings:
        print(f"Warning: {warning}")
    print(f"{len(regressions)} regressions were found")
    for regression in regressions:
        print(f"Regression: {regression}")
    if len(regressions) > 0:
        exit(1)


if __name__ == "__main__":
    main()
