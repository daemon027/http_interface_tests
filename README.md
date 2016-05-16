http interface tests
---------

## Overview

It's a simple test framework for http interface call, the flow likes:

---------
test-case-file(xml format) --> parser --> run --> validate --> test-report(junit format)
---------


Suppose you have a interface, when you call the interface(GET/POST), 
and the return value in json format likes: 

---------
{"a": 1, "b": "hello", "c": {"1": "c1", "c2": "hi"}}
---------

you can make your test case file like this:

---------
<test_case>
        <name>simple get interface test</name>
        <host_name>1.1.1.1:23456</host_name>
        <interface_name>/interface_a/b</interface_name>
        <http_method>GET</http_method>
        <input_data>
            <paramA>a</paramA>
            <paramB>1</paramB>
        </input_data>
        <expected_data>
            <a>1</a>
            <b>hello</b>
            <c__1>c1</c__1>
            <c__c2>hi</c__2>
        </expected_data>
</test_case>
---------

when the ruturn value in json format like this:

---------
[{"10":"test","bucket":["a1", "a2"],"id":"a1"},{"b":"prod","bucket":["4","3","2","1","0"],"id":3}]
---------

you can make your test case file like this:

---------
<test_case>
        <name>simple get interface test</name>
        <host_name>1.1.1.1:23456</host_name>
        <interface_name>/interface_a/b</interface_name>
        <http_method>POST</http_method>
        <input_data>
            <paramA>a</paramA>
            <paramB>1</paramB>
        </input_data>
        <expected_data>
            <!-- "9999" is  a fixed prefix before the real list index number,
                  to distinguish when the filed name is a number. -->
            <list__99990__10>test</list__99990__10>
            <list__99990__bucket__99990>a1</list__99990__bucket__99990>
            <list__99990__bucket__99991>a2</list__99990__bucket__99991>
            <list__99990__id>a1</list__99990__id>
            <list__99991__b>prod</list__99991__b>
            <list__99991__bucket__99990>4</list__99991__bucket__99990>
            <list__99991__bucket__99991>3</list__99991__bucket__99991>
            <list__99991__bucket__99992>2</list__99991__bucket__99992>
            <list__99991__bucket__99993>1</list__99991__bucket__99993>
            <list__99991__bucket__99990>0</list__99991__bucket__99990>
            <list__99990__id>3</list__99990__id>
        </expected_data>
</test_case>
---------


## Run
python run.py [test_suite.xml] [$HOST_IP]

The test case file and host ip are optional:
1. The default test case file is "test_suite.xml" if it's not specified.
2. The IP host is the host_name value in test case file if it's not specified.

