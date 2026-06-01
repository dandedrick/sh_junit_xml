#!/usr/bin/env python3
from inspect import signature

import click
from junit_xml import TestCase, TestSuite, to_xml_report_string


class StringOrFileContents(click.ParamType):
    name = "StringOrFileContents"

    def convert(self, value, param, ctx):
        if not isinstance(value, str):
            return value
        # If we start a string with @ we assume it is a file name and
        # open that file and pass the contents.
        if value.startswith("@"):
            fname = value[1:]
            value = open(fname, "r").read()
        return value


def generated_options_junit(func):
    for arg in signature(TestCase.__init__).parameters:
        if arg == "self":
            continue
        kwargs = {}
        match arg:
            case "elapsed_sec" | "assertions":
                kwargs["type"] = float
            case _:
                kwargs["type"] = StringOrFileContents()
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
        kwargs["type"] = StringOrFileContents()
        opt = click.option(f"--{name}", **kwargs)
        func = opt(func)
    return func


@click.command()
@generated_options_junit
@local_options_junit
@click.pass_context
def main(context, *args, **kwargs):
    # Build up the arguments for the TestCase constructor from the passed
    # arguments. We handle non-string arguments here (not all maybe be
    # handled).
    tc_args = {}
    params = context.params
    for arg, value in params.items():
        if value is None:
            continue
        if arg not in local_options:
            tc_args[arg] = value

    test_case = TestCase(**tc_args)
    if params.get("failure"):
        test_case.add_failure_info(params["failure"])
    if params.get("error"):
        test_case.add_error_info(params["error"])
    if params.get("skipped"):
        test_case.add_skipped_info(params["skipped"])
    suite = TestSuite(params["suite"], [test_case])
    if params.get("output"):
        with open(params["output"], "w") as f:
            f.write(to_xml_report_string([suite]))
    else:
        print(to_xml_report_string([suite]), end="")


if __name__ == "__main__":
    main()
