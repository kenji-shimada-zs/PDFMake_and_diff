#pip install Office365-REST-Python-Client
#pip install pypdf
#https://www.cfxlog.com/python-pypdf/
#担当は荒木さんか村上さん

#PDFフォルダ
#https://kyoceragp.sharepoint.com/sites/KWIC444/Shared Documents/Forms/AllItems.aspx?FolderCTID=0x012000EB8C1247BDBE6C45B68129C677F0436D&id=%2Fsites%2FKWIC444%2FShared%20Documents%2FGeneral%2F12%5F%E7%A0%94%E7%A9%B6%E3%83%86%E3%83%BC%E3%83%9E%EF%BC%8F%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E6%83%85%E5%A0%B1%2FK1302%2F04%5FDIGITAL%2F%E8%A8%AD%E8%A8%88%2FMAIN%E5%9F%BA%E6%9D%BF%2F%E5%9B%9E%E8%B7%AF%E5%9B%B3&viewid=d9a0e932%2D8104%2D4af3%2D9554%2D1666d0ebed9c
#回路図の並び順
#https://kyoceragp.sharepoint.com/:x:/r/sites/KWIC444/Shared Documents/General/12_%E7%A0%94%E7%A9%B6%E3%83%86%E3%83%BC%E3%83%9E%EF%BC%8F%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E6%83%85%E5%A0%B1/K1302/04_DIGITAL/%E8%A8%AD%E8%A8%88/MAIN%E5%9F%BA%E6%9D%BF/%E5%9B%9E%E8%B7%AF%E5%9B%B3/%E5%9B%9E%E8%B7%AF%E5%9B%B3%E4%BD%9C%E6%88%90%E9%80%A3%E7%B5%A1%E8%A1%A8.xlsx?d=w6f7fe1ec3dd24b48a3a34feb6c57c258&csf=1&web=1&e=qYCZg3
import pypdf,os,pathlib,datetime,argparse,subprocess
'''
PDFMerge
Uranus('//uranus/CR8000/design/Main_1/Main_1/Main_1.cir')以下の
すべての.shtファイルをPDFに変換し、一つのPDFファイルにまとめたうえ.py/.exe
と同じディレクトリに出力する
'''

#.sht->PDF変換ソフトの場所
ndpdf_path=pathlib.Path('C:/DesignGateway/zdg/bin/Win64/nbpdf.exe')
#time_info
cwd=pathlib.Path(os.getcwd())
#time_info
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
time_info = now.strftime('%Y%m%d_%H%M')

parser = argparse.ArgumentParser(description='PDFMerge') 
parser.add_argument('-s','--sht',help='.shtファイルの場所',default='//uranus/CR8000/design/FR1_Main/FR1_Main/FR1_Main.cir')
parser.add_argument('-o','--out',help='.pdf出力先'       ,default='./')
parser.add_argument('-t','--tmp',help='tempフォルダの場所',default='./temp')
args = parser.parse_args()  
sht_dir=pathlib.WindowsPath(f'{args.sht}')
out_dir=cwd.joinpath(f'{args.out}')
tmp_dir=cwd.joinpath(f'{args.tmp}')



def pdfMerge(sht_dir,out_dir,tmp_dir):
    print(f"sht_dir={sht_dir}")
    print(f"out_dir={out_dir}")
    print(f"tmp_dir={tmp_dir}")
    if out_dir.exists() == False:
        os.makedirs(out_dir)
    if tmp_dir.exists() == False:
        os.makedirs(tmp_dir)
    #初期化(tempフォルダ削除)
    temp_files=list(tmp_dir.glob("*.pdf"))
    for temp_file in temp_files:
        temp_file.unlink(missing_ok=True)

    sht_files=list(sht_dir.glob('*.sht'))

    #　sht→PDF変換@tmp
    for sht_file in sht_files:
        out_file=tmp_dir.joinpath(sht_file.with_suffix('.pdf').name)
        rtn = subprocess.run(f'{str(ndpdf_path)} -s -o "{str(out_file)}" "{str(sht_file)}"')
        if (rtn.returncode == 6):
            print(f'returncode={rtn.returncode} ライセンス数が上限になっています。')
            print('処理中止')
            input()
            exit()
        elif (rtn.returncode != 0):
            print(f'returncode={rtn.returncode} 不明なエラーです')
            print('処理中止')
            input()
            exit()
        elif (rtn.returncode == 0):
            print(f'{str(sht_file)} を処理中')
        else:
            print(f'returncode={rtn.returncode} 不明なエラーです')
            print('処理中止')
            input()
            exit()

    pdf_writer=pypdf.PdfWriter()
    temp_pdf_files = tmp_dir.glob("*.pdf")
    for temp_pdf_file in temp_pdf_files:
        temp_pdf = pypdf.PdfReader(temp_pdf_file)
        if len(temp_pdf.pages) == 1:
            pdf_writer.add_page(temp_pdf.pages[0])
        elif len(temp_pdf.pages) > 1:
            print(f'{temp_pdf.name} has {len(temp_pdf.pages)} pages:{str(temp_pdf)}')
            print(f'{temp_pdf.name} is skipped')
        else:
            print(f'{temp_pdf.name} has {len(temp_pdf.pages)} pages:{str(temp_pdf)}')
            print(f'{temp_pdf.name} is skipped')
    out_PDF_path=out_dir.joinpath(f'{time_info}.pdf')
    with open(out_PDF_path,"wb") as out_PDF_path:
        pdf_writer.write(out_PDF_path)
    print("Merge is finished")

if __name__ == "__main__":
    pdfMerge(sht_dir,out_dir,tmp_dir)

