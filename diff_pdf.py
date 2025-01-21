import sys,fitz,pathlib,os,shutil
import Marge_PDF_page
from pprint import pprint

UserDrive =pathlib.Path(f"{os.getenv('USERPROFILE')}")
cwd_path=pathlib.Path(os.getcwd())
pdf_old_path     = cwd_path.joinpath("test_pdf/MergedPDF_20241024_1016.pdf")
pdf_current_path = cwd_path.joinpath("test_pdf/MergedPDF_20241031_0903.pdf")
output_addr      = cwd_path.joinpath("output")
temp_addr        = UserDrive.joinpath('temp')

def diff(pdf_old_path:pathlib.Path,pdf_current_path:pathlib.Path,output_dir:pathlib.Path,temp_addr:pathlib.Path):
    if temp_addr.exists() == True:
        shutil.rmtree(temp_addr)

    if temp_addr.exists() == False:
        os.makedirs(temp_addr)

    pdf_old_doc    =fitz.open(pdf_old_path)
    pdf_current_doc=color_chg(fitz.open(pdf_current_path),color="red")
    pdf_old_doc_temp    =temp_addr.joinpath(f"{pdf_old_path.name}")
    pdf_current_doc_temp=temp_addr.joinpath(f"{pdf_current_path.name}")
    pdf_old_doc    .save(pdf_old_doc_temp)
    pdf_current_doc.save(pdf_current_doc_temp)
    Marge_PDF_page.merge_pdf_page(old_pdf=pdf_old_doc_temp,current_pdf=pdf_current_doc_temp,output_dir=output_dir)
    
def color_chg(doc_addr,color):
    doc = fitz.open(doc_addr)
    page = doc[3]

    for page in doc:
        if color=="red":
            color_chg_red(doc,page)
        elif color=="blue":
            color_chg_blue(doc,page)
        else:
            pass
    #doc.save(doc_addr.name)
    return doc
    
def color_chg_blue(doc,page):
    xref_lst = page.get_contents() 
    for xref in xref_lst:
        stream = doc.xref_stream(xref).decode()
        #print(stream)
        colorReplaced = stream \
            .replace('0 0 0 rg', '0 0 1 rg') \
            .replace('0 0 0 RG', '0 0 1 RG')
        cont = bytes(colorReplaced, "utf-8")
        doc.update_stream(xref, cont)

def color_chg_red(doc,page):
    xref_lst = page.get_contents() 
    for xref in xref_lst:
        stream = doc.xref_stream(xref).decode()
        #print(stream)
        colorReplaced = stream \
            .replace('0 0 0 rg', '1 0 0 rg') \
            .replace('0 0 0 RG', '1 0 0 RG')
        cont = bytes(colorReplaced, "utf-8")
        doc.update_stream(xref, cont)

if __name__== "__main__":
    PDF_files=list(cwd_path.glob('MergedPDF_*.pdf'))
    if len(PDF_files) == 0:
        print('Can not find pdf files')
        input()
    print(f'old_PDF_file=[{PDF_files[-2]}]')
    print(f'new_PDF_file=[{PDF_files[-1]}]')
    print('Start Check Diff........')
    diff(pdf_old_path=PDF_files[-2],pdf_current_path=PDF_files[-1],output_dir=output_addr,temp_addr=temp_addr)
    print('Finished')
    input()
