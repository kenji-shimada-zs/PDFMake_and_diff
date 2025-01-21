import diff_pdf as diff
import PDFMerge as PDFMerge
import pathlib,os

UserDrive =pathlib.Path(f"{os.getenv('USERPROFILE')}")
Onedrive  =UserDrive.joinpath("OneDrive - 京セラ株式会社")
k1303_main=Onedrive.joinpath("K1303\\04_DIGITAL\\検討\\MAIN基板")
circuit_design_path=k1303_main.joinpath("回路図")
if Onedrive.exists() and k1303_main.exists() and circuit_design_path.exists():
    pass
else:
    exit()

sht=pathlib.Path(r'Z:\design\FR1_Main\FR1_Main\FR1_Main.cir')
out=circuit_design_path
tmp=pathlib.Path(r'C:').joinpath('temp_CR8000')
os.makedirs(tmp,exist_ok=True)
PDFMerge.pdfMerge(sht_dir=sht,out_dir=out,tmp_dir=tmp)

PDF_files=list(out.glob('*.pdf'))
if len(PDF_files) == 0:
    print('Can not find pdf files')
print(f'old_PDF_file=[{PDF_files[-2]}]')
print(f'new_PDF_file=[{PDF_files[-1]}]')
diff.diff(pdf_old_path=PDF_files[-2],pdf_current_path=PDF_files[-1],output_dir=out,temp_addr=tmp)
print('Finished')    