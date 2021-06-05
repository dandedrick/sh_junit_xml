# sh_junit_xml
This a simple wrapper around the junit_xml python library to allow for
generating junit xml files from a shell. The main use case for this is
generating test results for jenkins from shell scripts.

## Installation
Install via pip:
```
pip install sh_junit_xml
```

Install from source:
```
./setup.py install
```

## Usage
The script wraps all arguments passed to `junit_xml.TestCase.__init__()` so
that you can construct any arbitrary test case that is available through this
class. The each argument is simply prepended with `--` and remains otherwise
identical. Most arguments are treated as strings but a few special cases are
converted after they are read in from the command line, such as `--elapsed_sec`
which is converted to a number since it is expected in that format.
Additionally arguments that start with `@` will be treated as filename, which
are opened and the contents are passed as the argument.

In addition to the automatic arguments generated from the TestCase constructor
the following arguments are available:
`--suite`: Specify the suite name
`--failure`: Mark the test as failed and pass the failure message.
`--error`: Mark the test as an error and pass the error message.
`--skipped`: Mark the test as skipped and pass the skipped message
