import datetime
import time

import testlink
from unittest import (
    TestCase,
    TestLoader,
    TextTestResult,
    TextTestRunner)
from pprint import pprint
import os

# import subprocess

# args = ["python", "test_module.py"]
# subprocess.call(args)
# tls.reportTCResult(a_TestCaseID, a_TestPlanID, 'a build name', 'f', 'some notes', user='a user login name', platformid=a_platformID)

# https://www.reddit.com/r/learnpython/comments/28eoz9/python_unittest_do_something_different_if_test/


# suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
# out = unittest.TextTestRunner(verbosity=2).run(suite)
# print (out)
from testing.test_simple import *

OK = 'ok'
FAIL = 'fail'
ERROR = 'error'
SKIP = 'skip'


class JsonTestResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super_class = super(JsonTestResult, self)
        super_class.__init__(stream, descriptions, verbosity)

        # TextTestResult has no successes attr
        self.successes = []

    def addSuccess(self, test):
        # addSuccess do nothing, so we need to overwrite it.
        super(JsonTestResult, self).addSuccess(test)
        self.successes.append(test)

    def json_append(self, test, result, out):
        suite = test.__class__.__name__
        if suite not in out:
            out[suite] = {OK: [], FAIL: [], ERROR: [], SKIP: []}
        if result is OK:
            out[suite][OK].append(test._testMethodName)
        elif result is FAIL:
            out[suite][FAIL].append(test._testMethodName)
        elif result is ERROR:
            out[suite][ERROR].append(test._testMethodName)
        elif result is SKIP:
            out[suite][SKIP].append(test._testMethodName)
        else:
            raise KeyError("No such result: {}".format(result))
        return out

    def jsonify(self):
        json_out = dict()
        for t in self.successes:
            json_out = self.json_append(t, OK, json_out)

        for t, _ in self.failures:
            json_out = self.json_append(t, FAIL, json_out)

        for t, _ in self.errors:
            json_out = self.json_append(t, ERROR, json_out)

        for t, _ in self.skipped:
            json_out = self.json_append(t, SKIP, json_out)

        return json_out



if __name__ == '__main__':
    # redirector default output of unittest to /dev/null
    with open(os.devnull, 'w') as null_stream:
        # new a runner and overwrite resultclass of runner
        runner = TextTestRunner(stream=null_stream)
        runner.resultclass = JsonTestResult

        # create a testsuite
        suite = TestLoader().loadTestsFromTestCase(TestSimple)

        # run the testsuite
        result = runner.run(suite)

        # print json output
        print(result.jsonify())
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        TESTLINK_API_PYTHON_SERVER_URL = "http://77.55.234.162:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
        TESTLINK_API_PYTHON_DEVKEY = "de221c3415cd566478274bbbe51ea42b"
        tlh = testlink.TestLinkHelper(TESTLINK_API_PYTHON_SERVER_URL, TESTLINK_API_PYTHON_DEVKEY)
        tls = testlink.TestlinkAPIClient(tlh._server_url, tlh._devkey, verbose=False)
        project_name = tls.getTestProjectByName("test of apartments library")['prefix']
        project_test_plan_id = tls.getTestPlanByName("test of apartments library","Testy biblioteki służącej do wyceny nieruchomości")['id']
        for ok in result.jsonify()['TestSimple']['ok']:
            tc_info = tls.getTestCaseIDByName(ok)
            tls.reportTCResult(None, project_test_plan_id, None, 'p', 'test passed', guess=True,
                               testcaseexternalid=str(project_name)+"-"+str(tc_info[0]['tc_external_id']),
                               platformname='NewPlatform',
                               execduration=3.9, timestamp=st)

        for fail in result.jsonify()['TestSimple']['fail']:
            tc_info = tls.getTestCaseIDByName(fail)
            tls.reportTCResult(None, project_test_plan_id, None, 'f', 'test failed', guess=True,
                               testcaseexternalid=str(project_name)+"-"+str(tc_info[0]['tc_external_id']),
                               platformname='NewPlatform',
                               execduration=3.9, timestamp=st)

        for error in result.jsonify()['TestSimple']['error']:
            tc_info = tls.getTestCaseIDByName(error)
            tls.reportTCResult(None, project_test_plan_id, None, 'b', 'test error', guess=True,
                               testcaseexternalid=str(project_name)+"-"+str(tc_info[0]['tc_external_id']),
                               platformname='NewPlatform',
                               execduration=3.9, timestamp=st)
        for skip in result.jsonify()['TestSimple']['skip']:
            print("Testy ominiete:"+str(skip))


