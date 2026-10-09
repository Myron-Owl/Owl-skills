"""Reusable fixture runner. Copies templates; never edits them. Choose one affected case."""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,json,shutil
from copy import copy
from edit_common import load_plan,digest,read_book,style
from native_operations import signature,rule_at,validation_map
from edit_native import execute

def run(fixtures,case):
    source=fixtures/'合并标签_保存兼容.xlsx'
    before=digest(source)
    with TemporaryDirectory(prefix='excel-common-') as tmp:
        root=Path(tmp);path=root/'case.xlsx';shutil.copy2(source,path)
        wb=read_book(path)
        p=dict(workbook=str(path),operations=[dict(sheet='基础模型',range='D8',kind='value',before=[[wb['基础模型']['D8'].value]],values=[[1.7]])],calculation='smart',
               acceptance=[dict(sheet='基础模型',range='H7',values=[[60/1.7]],tolerance=1e-8)])
        oldrule=signature(rule_at(wb['基础模型'],'D8'))
        expectedstyle=style(wb['基础模型']['H8'])
        originalvalidation=validation_map(wb['基础模型'])
        if case=='operations':
            p['format_copies']=[dict(sheet='基础模型',range='H9',source_sheet='基础模型',source_range='H8')]
            p['validations']=[dict(sheet='基础模型',cell='D8',before=oldrule,after=dict(type='decimal',operator='greaterThan',formula1='0',allowBlank=False,showErrorMessage=True,errorTitle='请输入正数',error='允许小数'))]
        wb.close()
        plan=root/'plan.json';plan.write_text(json.dumps(p),encoding='utf-8');p=load_plan(plan)
        class FormatExtension:
            def prepare(self,w,p):w['基础模型']['H9']._style=copy(w['基础模型']['H8']._style)
            def apply(self,w,p):
                s=w.Worksheets('基础模型');s.Range('H8').Copy();s.Range('H9').PasteSpecial(Paste=-4122);w.Application.CutCopyMode=False
            def verify_native(self,w,p):
                s=w.Worksheets('基础模型');assert s.Range('H9').NumberFormat==s.Range('H8').NumberFormat
        result=execute(p,FormatExtension() if case=='extension' else None)
        wb=read_book(path)
        if case=='operations':
            assert style(wb['基础模型']['H9'])==expectedstyle
            rules=validation_map(wb['基础模型']);assert rules['D8']['type']=='decimal'
            assert {k:v for k,v in rules.items() if k!='D8'}=={k:v for k,v in originalvalidation.items() if k!='D8'}
        if case=='extension':assert style(wb['基础模型']['H9'])==expectedstyle
        wb.close()
        assert digest(source)==before
        print(json.dumps(dict(case=case,status='PASS',restored_wrap=result['restored_merged_wrap'],seconds=result['timings_seconds']['total'])),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--fixtures',type=Path,required=True);ap.add_argument('--case',choices=['ordinary','operations','extension'],required=True)
    args=ap.parse_args();run(args.fixtures,args.case)
