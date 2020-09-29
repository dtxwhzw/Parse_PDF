import os
import sys

from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def get_white_paper(file_path):
    '''
    get all the white paper pdf
    for example, if you are using MacOS, the white_paer will return
    ['.DS_Store', 'ch-pe-project-description-final.pdf']
    so the '.DB_Store' should be removed from the file list
    :param file_path:
    :return:
    '''
    white_paper = os.listdir(file_path)
    if '.DS_Store' in white_paper:
        white_paper.remove('.DS_Store')
    return white_paper


def main(file_path,file_list):
    for file in file_list:
        pdf = open(file_path + '/' + file,'rb')
        parse = PDFParser(pdf)
        doc = PDFDocument()
        parse.set_document(doc)
        doc.set_parser(parse)
        # create PDF, explorer to share data
        rsrcmgr = PDFResourceManager()
        # create a PDF object
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in doc.get_pages() :
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout :
                if (isinstance(x, LTTextBoxHorizontal)) :
                    with open('./result/'+file+'.txt', 'a') as f :
                        results = x.get_text()
                        #print(results)
                        f.write(results + "\n")


if __name__ == "__main__":
    file_path = sys.argv[1]
    #file_path = './White Paper'
    files = get_white_paper(file_path)
    main(file_path,files)