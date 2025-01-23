import diff_pdf as diff
import PDFMerge as PDFMerge
import pathlib,os,subprocess,re,sys

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
PDF_files=[p for p in PDF_files if re.search(pattern='[0-9]{8}_[0-9]{4}.pdf',string=str(p))]
if len(PDF_files) == 0:
    print('Can not find pdf files')
def make_diff(old_PDF_file:pathlib.Path,new_PDF_file:pathlib.Path,out_diff_file:pathlib.Path):
    print(f'old_PDF_file={old_PDF_file}')
    print(f'new_PDF_file={new_PDF_file}')
    subprocess.run(f'diff-pdf --output-diff="{out_diff_file}" "{old_PDF_file}" "{new_PDF_file}"')
    #diff.diff(pdf_old_path=PDF_files[-2],pdf_current_path=PDF_files[-1],output_dir=out,temp_addr=tmp)

for i in range(1,len(PDF_files)):
    old_PDF_file=PDF_files[i-1]
    new_PDF_file=PDF_files[i  ]
    output_file_name=f'{old_PDF_file.stem}-{new_PDF_file.stem}_diff.pdf'
    output_file_path=out.joinpath(output_file_name)
    if output_file_path.exists() == False:
        make_diff(old_PDF_file=old_PDF_file,new_PDF_file=new_PDF_file,out_diff_file=output_file_path)

print('Finished')
sys.exit()
