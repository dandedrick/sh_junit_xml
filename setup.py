#!/usr/bin/env python3
import setuptools
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name='sh_junit_xml',
    version='1.0.0',
    py_modules=['sh_junit_xml'],
    entry_points={
        'console_scripts': [
            'sh_junit_xml = sh_junit_xml:main',
            ]
        },
    author='Dan Dedrick',
    author_email='dan.dedrick@gmail.com',
    description='A tool for generating junit output from a shell',
    install_requires=["junit_xml"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["sh_junit_xml"],
    python_requires='>=3',
    url="https://github.com/dandedrick/python-sh-junit-xml",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3"
        ]
    )
