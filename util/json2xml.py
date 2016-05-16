import json
import codecs
import traceback
import sys

reload(sys)
sys.setdefaultencoding('UTF8')

class json2xml:
    debug = 0
    def __init__(self, json_data, debug=0):
        self.debug = debug
        data_len = len(json_data)
        if(data_len == 0):
            print 'empty data'
            return
        else:
            for k in json_data.keys():
                self.build(k, json_data[k])

    def build(self, father_node, json_data):
        if type(json_data) == dict:
            for k in json_data:
                self.build(father_node + '__' + k, json_data[k])
        elif type(json_data) == list:
            list_num = 0
            for l in json_data:
                self.build(father_node + '__' + '9999' + str(list_num), l)
                list_num = list_num + 1
        else:
            if json_data == None:
                json_data = ''

            if self.debug == 1:
                print '[DEBUG]', father_node, ' => ', json_data

            if len(str(json_data)) > 0:
                print '<' + father_node + '>' + str(json_data) + '</' + father_node + '>'