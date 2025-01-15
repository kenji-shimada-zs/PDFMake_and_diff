import pypdf,pathlib,os,re

def merge_pdf_page(old_pdf,current_pdf,temp_dir):
    old_pdf_obj     = pypdf.PdfReader(old_pdf)
    current_pdf_obj = pypdf.PdfReader(current_pdf)
    output= pypdf.PdfWriter()
    for count in range(len(current_pdf_obj.pages)):
        current_pdf_obj.pages[count].merge_page(old_pdf_obj.pages[count],over=False)
        output.add_page(current_pdf_obj.pages[count])
    old_time=re.search('[\d]+_[\d]+',old_pdf.name).group()
    current_time=re.search('[\d]+_[\d]+',current_pdf.name).group()
    outStream = open(temp_dir.parent.joinpath(f'{old_time}-{current_time}_diff.pdf'),'wb')
    output.write(outStream)
    outStream.close()
    