#! /usr/bin/env python

import sys
import os
import glob
from pdfrw import PdfReader, PdfWriter
sys.path.insert(0, '..')
from autotest import checkmd5


dirnames = sys.argv[1:] or sorted(os.listdir('builds'))

filelist = []
extralist = []
for name in dirnames:
    dirname = 'builds/%s' % name
    assert os.path.exists(dirname)
    filelist += glob.glob('%s/*/*.pdf' % dirname)
    extralist += glob.glob('%s/*/*/*.pdf' % dirname)

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

def fixstuff(mylist, update_md5):
    for name in mylist:
        outname = name.replace('builds', 'fixed', 1)
        outdir = os.path.dirname(outname)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        if not os.path.isdir(name):
            try:
                fixone(name, outname)
            except Exception, s:
                print s
                continue
        if update_md5:
            md5name = os.path.basename(outname).replace('.pdf', '.json')
            md5name = '../md5/%s' % md5name

            result = checkmd5(name, md5name, [], False)
            if result in ('good', 'bad'):
                assert result == checkmd5(outname, md5name, [], result)

fixstuff(extralist, False)
fixstuff(filelist, True)
