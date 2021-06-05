#!/usr/bin/env python3
from inspect import signature
from argparse import ArgumentParser
from junit_xml import TestSuite, TestCase, to_xml_report_string


def main():
    parser = ArgumentParser(description="Generate junit test output")
    parser.add_argument('--suite')
    parser.add_argument('--failure')
    parser.add_argument('--error')
    parser.add_argument('--skipped')
    parser.add_argument('--output')

    # Dynamically add all parameters of the TestCase constructor. This gives us
    # the most flexibility with the least amount of work. Basic string
    # arguments will work by default. Other arguments may need special handling
    # a few have been done here already.
    test_args = []
    for arg in signature(TestCase.__init__).parameters:
        if arg == "self":
            continue
        parser.add_argument(f"--{arg}")
        test_args.append(arg)

    args = parser.parse_args()

    def arg_check_for_file(value):
        # If we start a string with @ we assume it is a file name and
        # open that file and pass the contents.
        if value.startswith("@"):
            fname = value[1:]
            value = open(fname, "r").read()
        return value

    # Build up the arguments for the TestCase constructor from the passed
    # arguments. We handle non-string arguments here (not all maybe be
    # handled).
    tc_args = {}
    for arg in test_args:
        if arg in args:
            value = getattr(args, arg)
            if value:
                value = arg_check_for_file(value)
                # The argument expects a number not a string so we have to
                # convert it here.
                if arg == "elapsed_sec" or arg == "assertions":
                    value = float(value)

                tc_args[arg] = value

    test_case = TestCase(**tc_args)
    if args.failure:
        test_case.add_failure_info(arg_check_for_file(args.failure))
    if args.error:
        test_case.add_error_info(arg_check_for_file(args.error))
    if args.skipped:
        test_case.add_skipped_info(arg_check_for_file(args.skipped))
    suite = TestSuite(args.suite, [test_case])
    if args.output:
        with open(args.output, "w") as f:
            f.write(to_xml_report_string([suite]))
    else:
        print(to_xml_report_string([suite]), end="")
