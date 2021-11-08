# -*- coding: utf-8 -*-

import json
import os
import sys


def parse_cyclo_log(log_path):
    average_complexity = 0
    complexity_baseline = os.getenv("COMPLEXITY_BASELINE")
    function_cyclo_details = []
    with open(log_path) as f:
        lines = f.readlines()
        average_complexity = lines[-1].split(" ")[-1]
        for line in lines[:-1]:
            each_line_items = line.split(" ")
            print(each_line_items)
            function_cyclo_details.append({
                "complexity": each_line_items[0],
                "pkg_name": each_line_items[1],
                "func_name": each_line_items[2],
                "position": each_line_items[3].rstrip()
            })

    return {
        "average_complexity": average_complexity,
        "complexity_baseline": complexity_baseline,
        "function_cyclo_details": function_cyclo_details,
        "summary": "{} functions exceed the cyclomatic quality gate ({})".format(len(function_cyclo_details),
                                                                                 complexity_baseline)
    }


if __name__ == '__main__':
    log_path = sys.argv[1]
    print("cyclo log path: ", log_path)

    os.environ["COMPLEXITY_BASELINE"] = "20"
    cyclo_data = parse_cyclo_log(log_path)
    str_cyclo_result = json.dumps(cyclo_data)
    str_cyclo_summary = json.dumps(cyclo_data.get("summary"))
    os.environ["ENV_CYCLO_RESULT"] = str_cyclo_result
    os.environ["ENV_CYCLO_SUMMARY"] = str_cyclo_summary
    with open("cyclo_result.json", "w") as f:
        f.write(str_cyclo_result)
    with open("cyclo_summary.info", "w") as f:
        f.write(str_cyclo_summary)

    print(os.getenv("ENV_CYCLO_RESULT"))

