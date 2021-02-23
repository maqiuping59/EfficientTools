import importlib
import sys
import time
import re
import pathlib
 

importlib.reload(sys)

import os.path
from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from PyPDF2 import PdfFileReader,PdfFileWriter


pattern=re.compile('[A-Z][A-Z] \d\d\d\d\d?-\d\d\d\d|[A-Z][A-Z] \d\d\d\d\d?-\d\d\d\d')


def parse(pdf_path):
    fp = open(pdf_path,'rb')
    parser = PDFParser(fp)
    #创建一个PDF文档
    doc = PDFDocument()
    #连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
 
    #提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()
 
    #检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr,laparams=laparams)
        #创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr,device)
 
        #循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            #接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if(isinstance(x,LTTextBoxHorizontal)):
                    results = x.get_text()
                    matchresult=re.findall(pattern,results)#利用正则表达式匹配标
                    if len(matchresult)!=0:
                        print("                       ",results,'   <========>    ',re.findall(pattern,results))


def splitPdf():
    defaultPath=pathlib.Path("inputs")#读取默认输入文件夹下的pdf文件
    for root,dirs,files in os.walk(defaultPath):
        for file in files:
            filename,externsion=os.path.splitext(file)
            print(filename,externsion)
            if externsion==".pdf":
                path=str(defaultPath)+"/"+filename+externsion
                pdf=PdfFileReader(path)
                for page in range(pdf.getNumPages()):
                    print("第",page,"页：    ")
                    pdf_writer=PdfFileWriter()
                    pdf_writer.addPage(pdf.getPage(page))
                    output = path=str(defaultPath)+"/"+filename+str(page)+externsion
                    with open(output, 'wb') as output_pdf:
                        pdf_writer.write(output_pdf)
                    parse(output)
                    os.remove(output)

 

                    
 
if __name__ == '__main__':
    splitPdf()

