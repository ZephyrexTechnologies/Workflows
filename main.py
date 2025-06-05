import json
import pathlib
from collections import defaultdict
import sys


def main():
    source_dict = defaultdict(list)
    dest_dict = defaultdict(list)
    source_fp = pathlib.Path(sys.argv[1])
    dest_fp = pathlib.Path(sys.argv[2])
    with open(source_fp, "r") as f:
        source_results = f.read().splitlines()[3:-1]  # Trim unnecessary entries
        for item in source_results:
            print(f"ITEM: {item}")
            json_data = json.loads(item)
            if "nodeid" in json_data.keys():
                source_dict[json_data["outcome"]].append(json_data["nodeid"])
    with open(dest_fp, "r") as f:
        dest_results = f.read().splitlines()[3:-1]  # Trim unnecessary entries
        for item in dest_results:
            json_data = json.loads(item)
            if "nodeid" in json_data.keys():
                dest_dict[json_data["outcome"]].append(json_data["nodeid"])
    regressions = []
    for item in dest_dict["passed"]:
        if item not in source_dict["passed"]:
            regressions.append(item)
    print(f"{len(regressions)} regressions were found")
    for item in regressions:
        print(f"Regression {item}")
    if len(regressions) > 0:
        exit(1)


if __name__ == "__main__":
    main()
