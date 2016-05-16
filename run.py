import xml.etree.ElementTree as ET
import traceback
import json
import re
import sys
import urllib
sys.path.append('util')
reload(sys)
sys.setdefaultencoding('UTF8')

from run_cmd import *
from validate_results import validate_results
from generate_test_report import generate_test_report

test_case_file = 'test_suite.xml'
host_name_in = None

input_param_len = len(sys.argv)
if input_param_len == 2:
    if sys.argv[1].endswith("xml"):
        test_case_file = sys.argv[1]
    else:
        host_name_in = sys.argv[1]
elif input_param_len == 3:
    test_case_file = sys.argv[1]
    host_name_in = sys.argv[2]

skipped_test_cases = []
passed_test_cases = []
failed_test_cases = {}

node = ET.parse(test_case_file)
root = node.getroot()

test_cases = root.findall('test_case')
call_url = None

test_err_code = 0

intermediate_data_dict = {} #store datea generated when running tests


for test_case in test_cases:
    data_dict = {}
    try:

        test_case_name = test_case.find('name').text
        interface_name = test_case.find('interface_name').text
        http_method = test_case.find('http_method').text
        if host_name_in != None:
            host_name = host_name_in
        else:
            host_name = test_case.find('host_name').text
        if host_name == None or interface_name == None:
            raise Exception('missing requried fields')

        print '***** run test', test_case_name, '*****'
        call_url = ' "http://' + host_name + interface_name + '?'
        for input_data in test_case.find('input_data'):
            call_url = call_url + input_data.tag + '=' + input_data.text + '&'
        #add the data generated in the running time
        if  interface_name.endswith('xxxx') or interface_name.endswith('yyyy') \
                or interface_name.endswith('zzzz') or 'abc' in interface_name \
                call_url = call_url + 'xxxx=' + intermediate_data_dict['ddddd']
        for expect_data in test_case.find('expected_data'):
            data_dict[expect_data.tag] = expect_data.text

        '''
        #chinese character
        if 'chinese_char' in input_data_keys: #url encoding chinese characters
            chinese_char = input_data_dict['accountName']
            if type(name_value) == unicode:
                name_str = 'accountName=' + urllib.quote(chinese_char_value.encode('utf-8'))
                input_data_str = re.sub('chinese_char=(.*?)&', name_str + '&', input_data_str)
        '''

        call_url = 'curl -X ' + http_method + ' "http://' + host_name + interface_name + '?' + input_data_str + '"'

        (ret, outs, errs) = run_cmd(call_url)

        if ret != 0:
            print '[FAIL] call url', call_url, 'failed!'
            failed_test_cases[test_case_name] = '[FAIL] call url ' + call_url + ' failed!'
        else:
            #store data generated in the running time to intermediate_data_dict
            if interface_name.endswith('xxxx'):
                if 'xxxx' in outs:
                    ret_data = json.loads(outs)
                    intermediate_data_dict['xxxx'] = ret_data.get('xxxx')

            #validation
            if len(data_dict) == 0:
                print 'Expected data is empty, skip validation for this test case, API returns:', outs
                passed_test_cases.append(test_case_name)
                continue
            else:
                (ret_code, validation_msg) = validate_results(outs, data_dict)
            #check validation results
            if ret_code != 0:
                print 'run case', test_case_name, 'failed'
                failed_test_cases[test_case_name] = validation_msg
            else:
                print 'run case', test_case_name, 'passed'
                passed_test_cases.append(test_case_name)

    except Exception as e:
        print '!!! exception when run test case, skip this case !!!', traceback.format_exc()
        if test_case_name == None:
            test_case_name = 'skipped'
        skipped_test_cases.append(test_case_name)
        continue

failed_tests = len(failed_test_cases)
skipped_tests = len(skipped_test_cases)
passed_tests = len(passed_test_cases)

if failed_tests != 0:
    print '***** total', failed_tests, 'test cases failed *****'
    for t in failed_test_cases:
        print t
    test_err_code = -1

print '***** total', passed_tests, 'test cases passed *****'
for t in passed_test_cases:
    print t

if skipped_tests != 0:
    print '***** total', skipped_tests, 'test cases were skipped *****'
    for t in skipped_test_cases:
        print t

generate_test_report(passed_test_cases, failed_test_cases)

exit(test_err_code)