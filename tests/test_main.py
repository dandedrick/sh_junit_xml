#!/usr/bin/env python3
import junit_xml
import os
import sh_junit_xml
import sys
from inspect import signature
from unittest.mock import patch
from io import StringIO
from tempfile import TemporaryDirectory


def test_all_test_case_args():
    argv = ["sh_junit_xml", "--suite", "test_suite"]
    for arg in signature(junit_xml.TestCase.__init__).parameters:
        if arg == "self":
            continue
        argv.append(f"--{arg}")
        if arg == "elapsed_sec" or arg == "assertions":
            argv.append("2")
        else:
            argv.append(arg)
    with patch.object(sys, "argv", argv):
        sh_junit_xml.main()


def test_failure():
    argv = ["sh_junit_xml", "--suite", "test_failure", "--name", "fail-test",
            "--classname", "fail.test", "--failure", "Test Failed"]
    with patch.object(sys, "argv", argv):
        with patch('sys.stdout', new=StringIO()) as xml_output:
            sh_junit_xml.main()
            with open("tests/xml_files/test_failure.xml", "r") as f:
                assert xml_output.getvalue() == f.read()


def test_error():
    argv = ["sh_junit_xml", "--suite", "test_error", "--name", "error-test",
            "--classname", "error.test", "--error", "Test Error", "--file",
            "foo.py", "--line", "123"]
    with patch.object(sys, "argv", argv):
        with patch('sys.stdout', new=StringIO()) as xml_output:
            sh_junit_xml.main()
            with open("tests/xml_files/test_error.xml", "r") as f:
                assert xml_output.getvalue() == f.read()


def test_skipped():
    argv = ["sh_junit_xml", "--suite", "test_skipped", "--name",
            "skipped-test", "--classname", "skipped.test", "--skipped",
            "@tests/input_files/skipped_reason", "--stdout",
            "@tests/input_files/skipped_stdout"]
    with patch.object(sys, "argv", argv):
        with patch('sys.stdout', new=StringIO()) as xml_output:
            sh_junit_xml.main()
            with open("tests/xml_files/test_skipped.xml", "r") as f:
                assert xml_output.getvalue() == f.read()


def test_passed():
    argv = ["sh_junit_xml", "--suite", "test_passed", "--name",
            "passed-test", "--classname", "passed.test"]
    with patch.object(sys, "argv", argv):
        with patch('sys.stdout', new=StringIO()) as xml_output:
            sh_junit_xml.main()
            with open("tests/xml_files/test_passed.xml", "r") as f:
                assert xml_output.getvalue() == f.read()

def test_passed_file():
    with TemporaryDirectory(prefix="squashfs_tmp_", dir="./") as temp:
        output_file = os.path.join(temp, "passed-test.xml")
        argv = ["sh_junit_xml", "--suite", "test_passed", "--name",
                "passed-test", "--classname", "passed.test", "--output",
                output_file]
        with patch.object(sys, "argv", argv):
            sh_junit_xml.main()
            with open("tests/xml_files/test_passed.xml", "r") as actual:
                with open(output_file, "r") as expected:
                    assert actual.read() == expected.read()
