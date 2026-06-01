#!/usr/bin/env python3
from inspect import signature

import click
from junit_xml import TestCase, TestSuite, to_xml_report_string


def generated_options_junit(func):
    for arg in signature(TestCase.__init__).parameters:
        if arg == "self":
            continue
        kwargs = {}
        match arg:
            case "elapsed_sec" | "assertions":
                kwargs["type"] = float
        opt = click.option(f"--{arg}", **kwargs)
        func = opt(func)
    return func


local_options = {"suite": {"required": True},
                 "failure": {},
                 "error": {},
                 "skipped": {},
                 "output": {}}


def local_options_junit(func):
    for name, kwargs in local_options.items():
        func = click.option(f"--{name}", **kwargs)(func)
    return func


@click.command()
@generated_options_junit
@local_options_junit
@click.pass_context
def main(context, *args, **kwargs):

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
    params = context.params
    for arg, value in params.items():
        if value is None:
            continue
        if arg not in local_options:
            tc_args[arg] = arg_check_for_file(value)

    test_case = TestCase(**tc_args)
    if params.get("failure"):
        test_case.add_failure_info(arg_check_for_file(params["failure"]))
    if params.get("error"):
        test_case.add_error_info(arg_check_for_file(params["error"]))
    if params.get("skipped"):
        test_case.add_skipped_info(arg_check_for_file(params["skipped"]))
    suite = TestSuite(params["suite"], [test_case])
    if params.get("output"):
        with open(params["output"], "w") as f:
            f.write(to_xml_report_string([suite]))
    else:
        print(to_xml_report_string([suite]), end="")


if __name__ == "__main__":
    main()
