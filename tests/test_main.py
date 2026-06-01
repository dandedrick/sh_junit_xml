#!/usr/bin/env python3
from inspect import signature
from pathlib import Path
from tempfile import TemporaryDirectory

import junit_xml
from click.testing import CliRunner

import sh_junit_xml


def test_all_test_case_args():
    argv = ["--suite", "test_suite"]
    for arg in signature(junit_xml.TestCase.__init__).parameters:
        if arg == "self":
            continue
        argv.append(f"--{arg}")
        if arg == "elapsed_sec" or arg == "assertions":
            argv.append("2")
        else:
            argv.append(arg)
    runner = CliRunner()
    result = runner.invoke(sh_junit_xml.main, argv)
    assert result.exit_code == 0


def test_failure():
    argv = ["--suite", "test_failure", "--name", "fail-test",
            "--classname", "fail.test", "--failure", "Test Failed"]
    runner = CliRunner()
    result = runner.invoke(sh_junit_xml.main, argv)
    assert result.exit_code == 0
    expected_output = Path("tests/xml_files/test_failure.xml").read_text()
    assert result.output == expected_output


def test_error():
    argv = ["--suite", "test_error", "--name", "error-test",
            "--classname", "error.test", "--error", "Test Error", "--file",
            "foo.py", "--line", "123"]
    runner = CliRunner()
    result = runner.invoke(sh_junit_xml.main, argv)
    assert result.exit_code == 0
    expected_output = Path("tests/xml_files/test_error.xml").read_text()
    assert result.output == expected_output


def test_skipped():
    argv = ["--suite", "test_skipped", "--name",
            "skipped-test", "--classname", "skipped.test", "--skipped",
            "@tests/input_files/skipped_reason", "--stdout",
            "@tests/input_files/skipped_stdout"]
    runner = CliRunner()
    result = runner.invoke(sh_junit_xml.main, argv)
    print(result.output)
    assert result.exit_code == 0
    expected_output = Path("tests/xml_files/test_skipped.xml").read_text()
    assert result.output == expected_output


def test_passed():
    argv = ["--suite", "test_passed", "--name",
            "passed-test", "--classname", "passed.test"]
    runner = CliRunner()
    result = runner.invoke(sh_junit_xml.main, argv)
    assert result.exit_code == 0
    expected_output = Path("tests/xml_files/test_passed.xml").read_text()
    assert result.output == expected_output


def test_passed_file():
    with TemporaryDirectory(prefix="squashfs_tmp_", dir="./") as temp:
        output_file = Path(temp) / "passed-test.xml"
        argv = ["--suite", "test_passed", "--name",
                "passed-test", "--classname", "passed.test", "--output",
                str(output_file)]
        runner = CliRunner()
        result = runner.invoke(sh_junit_xml.main, argv)
        assert result.exit_code == 0
        expected_output = Path("tests/xml_files/test_passed.xml").read_text()
        actual_output = output_file.read_text()
        assert actual_output == expected_output
