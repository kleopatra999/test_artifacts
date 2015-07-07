#! /usr/bin/env python

import sys
import os
import subprocess

prefix = 'https://rst2pdf-testing.s3.amazonaws.com'
locations = dict(
    radioactive = 'pmaupin/radioactive-rst2pdf-testing',
    rst2pdf = 'rst2pdf/rst2pdf'
)

build, buildnum, buildcount = sys.argv[1:]

for buildcount in range(1, int(buildcount) + 1):
    subdir = 'builds/%s_%s.%s' % (build, buildnum, buildcount)
    url = '%s/%s/%s/%s.%s/artifacts.zip' % (
          prefix, locations[build], buildnum, buildnum, buildcount)
    print(url)
    os.mkdir(subdir)
    os.chdir(subdir)
    subprocess.call(['wget', url])
    subprocess.call(['unzip', '-q', 'artifacts.zip'])
    subprocess.call(['rm', 'artifacts.zip'])
    os.chdir('../..')
