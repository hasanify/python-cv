#!/usr/bin/env python
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
import sys
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="python-cv"
)
mycursor = mydb.cursor()
# main


def main(argv):
    import getopt

    def usage():
        print(f'usage: {argv[0]} [-P password] [-o output] [-t text|html|xml|tag]'
              ' [-O output_dir] [-c encoding] [-s scale] [-R rotation]'
              ' [-Y normal|loose|exact] [-p pagenos] [-m maxpages]'
              ' [-S] [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin]'
              ' [-W word_margin] [-F boxes_flow] [-d] input.pdf ...')
        return 100
    try:
        (opts, args) = getopt.getopt(
            argv[1:], 'dP:o:t:O:c:s:R:Y:p:m:SCnAVM:W:L:F:')
    except getopt.GetoptError:
        return usage()
    if not args:
        return usage()
    # debug option
    debug = 0
    # input option
    password = b''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    encoding = 'utf-8'
    # pageno = 1
    scale = 1
    caching = True
    # showpageno = True
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
            pagenos.update(int(x)-1 for x in v.split(','))
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
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
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
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, laparams=laparams,
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
        return usage()
    for fname in args:
        with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, pagenos,
                                          maxpages=maxpages, password=password,
                                          caching=caching, check_extractable=True):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
    device.close()
    outfp.close()

    bad_words = ['Personal', 'Information',
                 'Projects', 'Internship', 'Technologies']
    with open('cv.txt') as oldfile, open('cv_new.txt', 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words):
                newfile.write(line)

    file = open("cv_new.txt", "r")
    s = file.read()
    s = s.split('\n')

    while("" in s):
        s.remove("")
    while(" " in s):
        s.remove(" ")
    while("\x0c" in s):
        s.remove("\x0c")

    details = []
    i = 0
    while(i < len(s)):
        s1 = s[i].split(': ')
        if(len(s1) > 1):
            details.append(s1[1])
        i += 1

    sql = "INSERT INTO entries (name, post, exp) VALUES (%s, %s, %s)"
    val = (details[0], details[1], details[2])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
