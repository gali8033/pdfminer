#!/usr/bin/env python
import sys
import getopt
import os
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
from pdfminer.chapterparser import ChapterParser


# main
def main(argv):
    setOptionsAndConvert(argv)


def usage(argv):
    print(f'usage: {argv[0]} '
          f'[-P password] '
          f'[-o output] '
          f'[-t text|html|xml|tag]'
          ' [-O output_dir] '
          '[-c encoding] '
          '[-s scale] [-R rotation] '
          '[-Y normal|loose|exact] '
          '[-p pagenos] '
          '[-m maxpages] '
          '[-S] [-C] [-n] [-A] [-V] '
          '[-M char_margin] '
          '[-L line_margin]'
          '[-W word_margin] '
          '[-F boxes_flow] '
          '[-d] '
          'input.pdf ...')
    return 100


def setOptionsAndConvert(argv):
    try:
        (opts, args) = getopt.getopt(argv[1:],
                                     'dP:o:t:TO:c:s:R:Y:p:m:SCnAVM:W:L:F:')
    except getopt.GetoptError:
        return usage(argv)
    if not args:
        return usage(argv)

    # debug option
    debug = 0
    # input option
    password = b''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    chapterSplit = False
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    encoding = 'utf-8'
    scale = 1
    caching = True

    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d':
            debug += 1
        elif k == '-P':
            password = v.encode('ascii')
        elif k == '-o':
            outfile = v
        elif k == '-t':
            outtype = v
        elif k == '-T':
            chapterSplit = True
        elif k == '-O':
            imagewriter = ImageWriter(v)
        elif k == '-c':
            encoding = v
        elif k == '-s':
            scale = float(v)
        elif k == '-R':
            rotation = int(v)
        elif k == '-Y':
            layoutmode = v
        elif k == '-p':
            pagenos.update(int(x) - 1 for x in v.split(','))
        elif k == '-m':
            maxpages = int(v)
        elif k == '-S':
            stripcontrol = True
        elif k == '-C':
            caching = False
        elif k == '-n':
            laparams = None
        elif k == '-A':
            laparams.all_texts = True
        elif k == '-V':
            laparams.detect_vertical = True
        elif k == '-M':
            laparams.char_margin = float(v)
        elif k == '-W':
            laparams.word_margin = float(v)
        elif k == '-L':
            laparams.line_margin = float(v)
        elif k == '-F':
            laparams.boxes_flow = float(v)
    pdfToText(args, debug, caching, outtype, outfile, encoding, laparams,
              imagewriter, stripcontrol, scale, layoutmode, pagenos,
              maxpages, password, rotation, chapterSplit)
    return (debug, caching, outtype, outfile, encoding, chapterSplit,
            imagewriter, stripcontrol, scale, layoutmode, pagenos,
            maxpages, password, rotation)


def pdfToText(args, debug, caching, outtype, outfile, encoding, laparams,
              imagewriter, stripcontrol, scale, layoutmode, pagenos,
              maxpages, password, rotation, chapterSplit):
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    rsrcmgr = PDFResourceManager(caching=caching)

    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = open(outfile, 'w', encoding=encoding)
    else:
        outfp = sys.stdout
        if chapterSplit:
            outfp = open('chaptersplit.txt', 'w', encoding=encoding)
        else:
            outfp = sys.stdout

    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, chapterSplit, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter, debug=debug)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp)
    else:
        return usage([])
    for fname in args:
        with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp,
                                          pagenos,
                                          maxpages=maxpages,
                                          password=password,
                                          caching=caching,
                                          check_extractable=True):
                page.rotate = (page.rotate + rotation) % 360

                interpreter.process_page(page)

    device.close()
    outfp.close()
    if chapterSplit:
        cp = ChapterParser()
        cp.split_chapters('chaptersplit.txt', '')
        os.remove('chaptersplit.txt')

    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
