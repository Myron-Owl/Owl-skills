"""Fast development checks for validation scope and format inheritance; no Excel."""
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from native_operations import prepare, signature, validation_map
from edit_common import EditError,style
from native_preservation import extension_guard,capture_protected,verify_protected

def run():
    w=Workbook();s=w.active;s.title='Data';s['A1']=2;s['B1']=5;s['B1'].font=Font(name='Arial',size=11,bold=True)
    d=DataValidation(type='whole',operator='between',formula1='1',formula2='100');d.add('A1:A3');s.add_data_validation(d)
    old=validation_map(s)
    p={'format_copies':[dict(sheet='Data',range='C1',source_sheet='Data',source_range='B1')],
       'validations':[dict(sheet='Data',cell='A1',before=signature(d),after=dict(type='decimal',operator='greaterThan',formula1='0'))]}
    prepare(w,p)
    assert s['C1'].value is None and style(s['C1'])==style(s['B1'])
    now=validation_map(s);assert now['A1']['type']=='decimal' and now['A2']==old['A2'] and now['A3']==old['A3']
    try:prepare(w,p)
    except EditError:pass
    else:raise AssertionError('Stale validation before accepted')
    d=DataValidation(type='custom',formula1='A4>0');d.add('A4:A6');s.add_data_validation(d)
    p={'validations':[dict(sheet='Data',cell='A4',before=signature(d),after=dict(type='decimal',formula1='0'))]}
    try:prepare(w,p)
    except EditError:pass
    else:raise AssertionError('Relative shared rule silently split')
    guard=extension_guard(w);s['B1']=99;assert extension_guard(w)!=guard
    protected=capture_protected(w,full=True)
    s['B1'].font=Font(size=40)
    try:verify_protected(w,protected,{'operations':[]})
    except EditError:pass
    else:raise AssertionError('Unrequested font change accepted')
    w.close();print('PASS: shared numeric rule split, untouched neighbors, stale before rejection, relative-rule rejection, format-only copy, extension guard')

if __name__=='__main__':run()
