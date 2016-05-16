import json
import urllib
import codecs
import string
import sys
import traceback
import re

reload(sys)
sys.setdefaultencoding('UTF8')

def get_json_value(json_data, json_key):
    fields = json_key.split('__')
    value = json_data.get(fields[0])
    try:
        for i in range(1, len(fields)):
            k = fields[i]

            if k.isdigit() == False:
                value = value.get(k)
            elif k.isdigit() == True and k.startswith('9999'):
                value = value[string.atoi(k[4:], 10)]
            else:
                value = value.get(k)

            #value = value.get(k)
    except Exception:
        print '!!! the actual data is wrong !!!'
        #print 'json data:', json_data
        return ''

    return value

def validate_json_data(output_json_string, expected_data_dict):
    ret_code = 0
    json_data = 'ERROR'
    validation_err_msg = ''
    if output_json_string.startswith('SPECIAL_PREFIX_'):
        output_json_string = (re.split('SPECIAL_PREFIX_\w+\(', output_json_string)[1]).split(')')[0]
    if output_json_string.startswith('%'):
        output_json_string = urllib.unquote(output_json_string)
    if output_json_string.startswith('[') and output_json_string.endswith(']'):
        output_json_string = '{"list":' + output_json_string + '}'
    try:
        json_data = json.loads(output_json_string)
    except Exception:
        print '!!! the return json data is wrong !!!'
        print 'return json data: ', json_data
        validation_err_msg = validation_err_msg + 'return wrong json data:\n' + json_data + '\n'
        ret_code = ret_code + 1
        return (ret_code, validation_err_msg)
    for key in expected_data_dict:
        json_value = get_json_value(json_data, key)
        if str(json_value) != expected_data_dict[key]:
            print '!!! field', key, 'COMPARE FAIL !!!, output vs expected:',  json_value, 'vs', expected_data_dict[key]
            validation_err_msg = validation_err_msg + '!!! field ' + key + ' COMPARE FAIL !!!, output vs expected: ' + str(json_value) + ' vs ' + expected_data_dict[key] + '\n'
            ret_code = ret_code + 1

    return (ret_code, validation_err_msg)

def validate_text_data(output_text, expected_data_dict):
    ret_code = 0
    validation_err_msg = ''
    if output_text != expected_data_dict['text']:
        print '!!! raw text result validation failed !!!, output vs expected:', output_text, 'vs', expected_data_dict['text']
        validation_err_msg = '!!! raw text result validation failed !!!, output vs expected:' + output_text + 'vs', expected_data_dict['text'] + '\n'
        ret_code = ret_code + 1

    return (ret_code, validation_err_msg)

def validate_results(output_string, expected_data_dict):
    if (output_string.startswith('{') and output_string.endswith('}')) or (output_string.startswith('[') and output_string.endswith(']')):
        return validate_json_data(output_string, expected_data_dict)
    else:
        return validate_text_data(output_string, expected_data_dict)