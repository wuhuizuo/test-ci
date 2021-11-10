# -*- coding: utf-8 -*-

import json
import sys
from xml.etree import ElementTree as ET

if __name__ == '__main__':
    report_path = sys.argv[1]
    print("test report path: ", report_path)
    tree = ET.parse(report_path)
    root = tree.getroot()

    count_total_test_case = 0
    count_failure_test_case = 0
    count_success_test_case = 0
    for p in root.findall('./testsuite'):
        count_total_test_case += int(p.attrib.get("tests"))
        count_failure_test_case += int(p.attrib.get("failures"))

    count_success_test_case = count_total_test_case - count_failure_test_case
    summary_info = "failure [{}], success [{}], total [{}]".format(count_failure_test_case,
                                                                   count_success_test_case,
                                                                   count_total_test_case)
    print(summary_info)
    with open("test_summary.info", "w") as f:
        f.write(json.dumps(summary_info))
