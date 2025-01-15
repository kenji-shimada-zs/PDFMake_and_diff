import tools.diff_pdf as diff
import tools.PDFMerge as PDFMerge
import pathlib

sht=pathlib.Path('Z:\design\FR1_Main\FR1_Main\FR1_Main.cir')
out=pathlib.Path('Z:\design\FR1_Main\回路図')
tmp=pathlib.Path('Z:\design\FR1_Main\回路図\tmp')
PDFMerge.pdfMerge(sht_dir=sht,out_dir=out,tmp_dir=tmp)
pass