import datetime
import json
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
            json_unit = {
                test._testMethodName: {
                    'when_clock_started': datetime.datetime.fromtimestamp
                    (test.clock_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'when_clock_ended': datetime.datetime.fromtimestamp
                    (test.clock_end).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'time_of_execution': test.execution_clock,
                    'status_of_testCase': "passed"
                }}
            out[suite][OK].append(json_unit)
        elif result is FAIL:
            unit_test = {
                test._testMethodName: {
                    'when_clock_started': datetime.datetime.fromtimestamp
                    (test.clock_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'when_clock_ended': "-",
                    'time_of_execution': "-",
                    'status_of_testCase': "blocked"
                }}
            out[suite][FAIL].append(unit_test)
        elif result is ERROR:
            json_unit = {
                test._testMethodName: {
                    'when_clock_started': datetime.datetime.fromtimestamp
                    (test.clock_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'when_clock_ended': "-",
                    'time_of_execution': "-",
                    'status_of_testCase': "failed"
                }}
            out[suite][ERROR].append(json_unit)
        elif result is SKIP:
            json_unit = {
                test._testMethodName: {
                    'when_clock_started': datetime.datetime.fromtimestamp
                    (test.clock_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'when_clock_ended': "-",
                    'time_of_execution': "-",
                    'status_of_testCase': "skipped"
                }}
            out[suite][SKIP].append(json_unit)
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
        project_name = tls.getTestProjectByName("test of apartments application")['prefix']

        project_test_plan_id = \
            tls.getTestPlanByName("test of apartments application", "Tests of application used to valuate apartments")[
                0][
                'id']

        for ok in result.jsonify()['TestSimple']['ok']:
            print()
            tc_info = tls.getTestCaseIDByName(list(ok.keys())[0])
            print(tc_info)
            tc_id = tls.getTestCaseIDByName(list(ok.keys())[0])[0]['id']
            tls.reportTCResult(tc_id, project_test_plan_id, None, 'p',
                               'test executed successfully. Started at: ' + str(
                                   list(ok.values())[0]['when_clock_started']) + ".More details in attached file",
                               guess=True,
                               testcaseexternalid=str(project_name) + "-" + str(tc_info[0]['tc_external_id']),
                               platformname='Python 3',
                               execduration=list(ok.values())[0][
                                   'time_of_execution'], timestamp=st, user="patrykz8")
            last_exec_id = tls.getLastExecutionResult(project_test_plan_id, tc_id)[0]['id']
            with open('json_file', 'w') as outfile:
                json.dump(ok, outfile)

            tls.uploadExecutionAttachment('json_file', last_exec_id, "details", "json file with test details")

        for fail in result.jsonify()['TestSimple']['fail']:
            tc_info = tls.getTestCaseIDByName(list(fail.keys())[0])
            tc_id = tls.getTestCaseIDByName(list(fail.keys())[0])[0]['id']

            tls.reportTCResult(tc_id, project_test_plan_id, None, 'f', 'test executed with fail. Started at: ' + str(
                list(fail.values())[0]['when_clock_started']) + ".More details in attached file", guess=True,
                               testcaseexternalid=str(project_name) + "-" + str(tc_info[0]['tc_external_id']),
                               platformname='Python 3',
                               execduration=list(fail.values())[0][
                                   'time_of_execution'], timestamp=st, user="patrykz8")
            last_exec_id = tls.getLastExecutionResult(project_test_plan_id, tc_id)[0]['id']
            with open('json_file', 'w') as outfile:
                json.dump(fail, outfile)

            tls.uploadExecutionAttachment('json_file', last_exec_id, "details", "json file with test details")

        for error in result.jsonify()['TestSimple']['error']:
            tc_info = tls.getTestCaseIDByName(list(error.keys())[0])
            tc_id = tls.getTestCaseIDByName(list(error.keys())[0])[0]['id']
            tls.reportTCResult(tc_id, project_test_plan_id, None, 'b', 'test executed with error.' + str(
                list(error.values())[0]['when_clock_started']) + ".More details in attached file", guess=True,
                               testcaseexternalid=str(project_name) + "-" + str(tc_info[0]['tc_external_id']),
                               platformname='Python 3',
                               execduration=list(error.values())[0][
                                   'time_of_execution'], timestamp=st, user="patrykz8")
            last_exec_id = tls.getLastExecutionResult(project_test_plan_id, tc_id)[0]['id']
            with open('json_file', 'w') as outfile:
                json.dump(error, outfile)

            tls.uploadExecutionAttachment('json_file', last_exec_id, "details", "json file with test details")

        for skip in result.jsonify()['TestSimple']['skip']:
            print("Testy ominiete:" + str(skip))
