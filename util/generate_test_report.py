import traceback

def generate_test_report(passed_test_cases, failed_test_cases):
    total_case_num = len(passed_test_cases) + len(failed_test_cases)
    test_report_file_name = 'function_test_report.xml'
    try:
        test_report_file_obj = open(test_report_file_name, 'w')
        test_report_file_obj.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        test_report_file_obj.write('<testsuites>\n')
        test_report_file_obj.write('<testsuite name="XXXXX.functionalTests" tests="'+ str(total_case_num) + '">\n')
        for passed_case in passed_test_cases:
            test_report_file_obj.write('<testcase name="' + passed_case + '"/>\n')
        for failed_case in failed_test_cases.keys():
            test_report_file_obj.write('<testcase name="' + failed_case + '">\n')
            test_report_file_obj.write('<failure type="error">' + failed_test_cases[failed_case].replace('&', '&amp;') + '</failure>\n')
            test_report_file_obj.write('</testcase>\n')
        test_report_file_obj.write('</testsuite>\n')
        test_report_file_obj.write('</testsuites>\n')
    except Exception:
        print '[FAIL] generate test report file failed!', traceback.format_exc()

    test_report_file_obj.close()