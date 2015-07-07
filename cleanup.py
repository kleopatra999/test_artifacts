#! /usr/bin/env python

import sys
import os
import glob
from pdfrw import PdfReader, PdfWriter

dirnames = sys.argv[1:] or sorted(os.listdir(build))

filelist = []
for name in dirnames:
    dirname = 'builds/%s' % name
    assert os.path.exists(dirname)
    filelist += glob.glob('%s/*.pdf' % dirname)
    filelist += glob.glob('%s/*/*.pdf' % dirname)

def fixone(srcf, dstf):
    print(srcf)
    trailer = PdfReader(srcf)
    trailer.Info = None  # Kill metadata
    prefix = 'file:///home/travis/build/rst2pdf/rst2pdf/rst2pdf/tests'

    for page in trailer.pages:
        annots = page.Annots
        if annots is None:
            continue
        for annot in annots:
            a = annot.A
            if a is None:
                continue
            uri = a.URI
            if uri is None:
                continue
            uri = uri.decode()
            if not uri.startswith('file:///'):
                continue
            a.URI = prefix + uri.split('rst2pdf/tests', 1)[-1]

    PdfWriter().write(dstf, trailer)

for name in filelist:
    if os.path.isdir(name):
        continue
    outname = name.replace('builds', 'fixed', 1)
    outdir = os.path.dirname(outname)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        fixone(name, outname)
    except Exception, s:
        print s
