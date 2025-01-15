import tools.diff_pdf as diff
import tools.PDFMerge as PDFMerge
import pathlib

sht=pathlib.Path(r'Z:\design\FR1_Main\FR1_Main\FR1_Main.cir')
out=pathlib.Path(r'Z:\design\FR1_Main\回路図')
tmp=pathlib.Path(r'Z:\design\FR1_Main\回路図\tmp')
PDFMerge.pdfMerge(sht_dir=sht,out_dir=out,tmp_dir=tmp)

PDF_files=list(out.glob('*.pdf'))
if len(PDF_files) == 0:
    print('Can not find pdf files')
print(f'old_PDF_file=[{PDF_files[-2]}]')
print(f'new_PDF_file=[{PDF_files[-1]}]')
diff(pdf_old_path=PDF_files[-2],pdf_current_path=PDF_files[-1],temp_addr=temp_addr)
print('Finished')    