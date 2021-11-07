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
                "complexity": each_line_items[1],
                "pkg_name": each_line_items[2],
                "func_name": each_line_items[3],
                "position": each_line_items[4].rstrip()
            })

    str_cyclo_result = json.dumps({
        "average_complexity": average_complexity,
        "complexity_baseline": complexity_baseline,
        "function_cyclo_details": function_cyclo_details,
        "summary": "{} functions exceed the cyclomatic quality gate ({})".format(len(function_cyclo_details),
                                                                                 complexity_baseline)
    })

    return str_cyclo_result


if __name__ == '__main__':
    log_path = sys.argv[1]
    print("cyclo log path: ", log_path)

    os.environ["COMPLEXITY_BASELINE"] = "20"
    str_cyclo_result = parse_cyclo_log(log_path)
    os.environ["ENV_CYCLO_RESULT"] = str_cyclo_result
    with open("gocyclo_result.json", "w") as f:
        f.write(str_cyclo_result)

    print(os.getenv("ENV_CYCLO_RESULT"))






# result_data = {
#     "average_complexity": 4.44,
#     "complexity_baseline": 20,
#     "function_cyclo_details": [{
#         "complexity": 2072,
#         "pkg_name": "",
#         "fun_cname": "",
#         "position": "",
#     }]
# }
