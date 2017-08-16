#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
from __future__ import unicode_literals
import os
import re
import sys
import math
import time
import random
import keyword
from math import *
from random import *
from ExerciseGeneratorDlg import *
#from sudoku_maker import SudokuMaker
import sudokulib
import sudokulib.sudoku
from sudokulib.sudoku import Sudoku
import pypinyin
from pypinyin import pinyin, lazy_pinyin

ABOUT_INFO = '''\
Python自动出题程序 V1.2
将生成结果复制粘帖到Excel/WPS中排版

规则说明：
1. 定义必须包含generator函数，其返回值必须为字符串列表，作为单次出题结果。
2. 用ASSERT函数筛除不符合规则的出题。
3. 用STOP函数结束出题循环。
4. math/random库的所有函数已导入，可直接使用。
6. 支持pypinyin库，可直接使用pinyin，lazy_pinyin函数。
6. 支持unicode字符串。
7. 当返回结果项为字符串“EOL”时，换行输出。
8. 用load_cn_words函数从UTF8编码的TXT文件加载词语，词语间用空格或换行分隔，忽略#开头的注释部分，忽略~开头的词语。

URL: https://github.com/pengshulin/exercise_generator
Peng Shullin <trees_peng@163.com> 2017
'''

CONFIGS_LIST = [
['生成随机数', '''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    return [ a ]
'''],

['生成整行随机数', '''\
def generator():
    l, LINE_LIMIT = '', 50
    while len(l) < LINE_LIMIT:
        #l = l + str(randint(0, 9))
        #l = l + str(randint(0, 9)) + ' '
        l = l + str(randint(10, 99)) + ' '
        #l = l + str(randint(100, 999)) + ' '
    return [ l ]
'''],


['加减法（2个数）', '''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    oper = choice( '+-' ) 
    if oper == '+':
        c = a + b
        jinwei = bool( a%10 + b%10 >= 10 )
        #ASSERT( jinwei )  # 进位
        #ASSERT( not jinwei )  # 不进位
    else:
        c = a - b
        tuiwei = bool( a%10 < b%10 )
        #ASSERT( tuiwei )  # 退位
        #ASSERT( not tuiwei )  # 不退位
    ASSERT( 0 <= c <= MAX )
    #return [ a, oper, b, '=', '□' ]
    #return [ '%s%s%s='% (a, oper, b) ] 
    #return [ '%s%s%s='% (a, oper, b), c ] 
    #return [ '%s%s%s'% (a, oper, b), '=', c ] 
    #return [ a, oper, '□', '=', c  ]
    return [ a, oper, b, '=', c ]
'''],

['乘法（2个数）', '''\
def generator():
    MIN, MAX = 1, 10
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    c = a * b
    ASSERT( 0 <= c <= 100 )
    return [ a, '*', b, '=', c ]
'''],

['比较大小（2个数）', '''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    if a > b:
        oper = '>'
    elif a < b:
        oper = '<'
    else:
        oper = '='
    #return [ a, '○', b ]
    return [ a, oper, b ]
'''],

['连加连减（3个数）', '''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    c = randint(MIN, MAX)
    oper1 = choice( '+-' ) 
    oper2 = choice( '+-' ) 
    if oper1 == '+':
        ab = a + b
    else:
        ab = a - b
    ASSERT( 0 <= ab <= MAX )
    if oper2 == '+':
        d = ab + c
    else:
        d = ab - c 
    ASSERT( 0 <= d <= MAX )
    #return [ '%s%s%s%s%s=%s'% (a, oper1, b, oper2, c, d) ]
    #return [ '%s%s%s%s%s='% (a, oper1, b, oper2, c) ]
    return [ a, oper1, b, oper2, c, '=', d ]
'''],

['三角分解', '''\
def generator():
    MIN, MAX = 0, 20
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    c = randint(MIN, MAX)
    ab = a + b
    bc = b + c
    ac = a + c
    ASSERT( 0 <= ab <= MAX )
    ASSERT( 0 <= bc <= MAX )
    ASSERT( 0 <= ac <= MAX )
    return [ 'EOL','EOL',ab,'',a,'',ac,'EOL','EOL','',b,'',c,'EOL','EOL','','',bc]
'''],


['数墙（3层）', '''\
def generator():
    MIN, MAX = 0, 20
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    c = randint(MIN, MAX)
    ab = a + b
    bc = b + c
    abc = ab + bc
    ASSERT( 0 <= ab <= MAX )
    ASSERT( 0 <= bc <= MAX )
    ASSERT( 0 <= abc <= MAX )
    return [ 'EOL','','',abc,'EOL','',ab,'',bc,'EOL',a,'',b,'',c]
'''],

['数墙（4层）', '''\
def generator():
    MIN, MAX = 0, 20
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    c = randint(MIN, MAX)
    d = randint(MIN, MAX)
    ab = a + b
    bc = b + c
    cd = c + d
    abc = ab + bc
    bcd = bc + cd
    abcd = abc + bcd
    ASSERT( 0 <= ab <= MAX )
    ASSERT( 0 <= bc <= MAX )
    ASSERT( 0 <= cd <= MAX )
    ASSERT( 0 <= abc <= MAX )
    ASSERT( 0 <= bcd <= MAX )
    ASSERT( 0 <= abcd <= MAX )
    return [ 'EOL','','','',abcd,'EOL','','',abc,'',bcd,'EOL','',ab,'',bc,'',cd,'EOL',a,'',b,'',c,'',d]
'''],

['排序（4个数）', '''\
def generator():
    MIN, MAX = 0, 100
    lst = [randint(MIN, MAX) for i in range(4)]
    lst.sort()
    a, b, c, d = lst
    ASSERT( a < b < c < d )
    #r=[a,b,c,d]; shuffle(r); return r
    return [ a, '<', b, '<', c, '<', d ]
'''],

['排序（5个数）', '''\
def generator():
    MIN, MAX = 0, 100
    lst = [randint(MIN, MAX) for i in range(5)]
    lst.sort()
    a, b, c, d, e = lst
    ASSERT( a < b < c < d < e )
    r=[a,b,c,d,e]; shuffle(r); s=', '.join(map(str,r))
    return [ s, '>'.join(['____']*5) ]
'''],

['算术题排序（5个算术题）', '''\
def generator():
    MIN, MAX = 0, 20
    def generate_single():
        a, b = randint(MIN, MAX), randint(MIN, MAX)
        return (a,b,a+b)

    a1, a2, a = generate_single()  
    ASSERT( MIN <= a <= MAX )
    b1, b2, b = generate_single()  
    ASSERT( MIN <= b <= MAX )
    ASSERT( b != a )
    c1, c2, c = generate_single()  
    ASSERT( MIN <= c <= MAX )
    ASSERT( c not in [a,b] )
    d1, d2, d = generate_single()  
    ASSERT( MIN <= d <= MAX )
    ASSERT( d not in [a,b,c] )
    e1, e2, e = generate_single()  
    ASSERT( MIN <= e <= MAX )
    ASSERT( e not in [a,b,c,d] )

    r=[[a1,a2],[b1,b2],[c1,c2],[d1,d2],[e1,e2]]
    shuffle(r)
    s=', '.join(['%s+%s'% (x,y) for x,y in r])
    return [ s, '>'.join(['________']*5) ]
'''],

['凑整数', '''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    ASSERT( 1 <= b <= 9 )
    #oper = choice( '+-' ) 
    oper = '+'
    if oper == '+':
        c = a + b
    else:
        c = a - b
    ASSERT( 10 <= c <= MAX )
    ASSERT( c % 10 == 0 )
    return [ a, oper, b, '=', c ]
'''],

['带拼音汉字抄写', '''\
source = load_cn_words('e:\文档\自动出题\词语默写.txt')
#source=list(''.join(source)) # 紧缩模式

copies=1
if copies > 1:
    source=[i*copies for i in source]  # 创建副本

columns, rows = 13, 11  # 控制每页行列
page_limit = 10  # 控制输出页数
row_cur, page_cur = 1, 1
def generator():
    global source, columns, rows, row_cur, page_cur, page_limit
    if not source or page_cur > page_limit:
        STOP()
    word = source.pop(0)[:columns]
    pinyin_lst = [i[0] for i in pinyin(word)]
    hanzi_lst = list(word)
    space_lst=[' ' for i in range(columns-len(word))]
    ret = pinyin_lst + space_lst + ['EOL'] + hanzi_lst + space_lst
    row_cur += 1
    if row_cur > rows:
        row_cur = 1
        page_cur += 1
    return ret
'''],

['看拼音默写词语', '''\
source = load_cn_words('e:\文档\自动出题\词语默写.txt')
#shuffle(source)  # 打乱顺序

columns, rows = 15, 11  # 控制每页行列
page_limit = 10  # 控制输出页数
row_cur, page_cur = 1, 1
def generator():
    global source, columns, rows, row_cur, page_cur, page_limit
    if not source or page_cur > page_limit:
        STOP()
    pinyin_lst, hanzi_lst, hanzi_blank_lst = [], [], []
    while True:
        if not source:
            break
        word = source.pop(0)
        word1 = ' ' + word
        hanzi_word = ''
        if len(pinyin_lst) + len(word1) <= columns:
            pinyin_lst += [i[0] for i in pinyin(word1)]
            hanzi_lst += list(word)
            hanzi_word +='('
            j = 0
            while j < len(word):
                hanzi_word += ' '
                j+=1
            hanzi_word += ')'
            hanzi_blank_lst+=list(hanzi_word)
            if len(pinyin_lst) + 1 < columns:
                pinyin_lst.append(' ')
                hanzi_lst.append(' ')
        else:
            source.insert(0, word)
            break
    while len(pinyin_lst) < columns:
        pinyin_lst.append(' ')
        hanzi_lst.append(' ')
    row_cur += 1
    if row_cur > rows:
        row_cur = 1
        page_cur += 1
    # 选择输出内容
    #return pinyin_lst + ['EOL'] + hanzi_lst  # 拼音+汉字
    #return ['EOL'] + hanzi_lst  # 仅汉字
    #return pinyin_lst + ['EOL']  # 仅拼音
    return pinyin_lst + ['EOL'] + ['EOL'] + hanzi_blank_lst + ['EOL']   # 拼音+汉字空格 [老婆要求 :( ] 
'''],


['舒尔特方格', '''\
size=5

def generator():
    global size
    source = range(1,size**2+1)
    shuffle(source)
    ret = []
    for i in range(size):
        ret += [ '%s'% source.pop() for j in range(size) ]
        ret.append('EOL')
    return ret
'''],


['人民币计算', '''\
def generator():
    MIN, MAX = 0.1, 10.0
    a = round(random()*MAX, 1)
    b = round(random()*MAX, 1)
    oper = choice( '+-' )
    if oper == '+':
        c = a + b
    else:
        c = a - b
    ASSERT( MIN <= a <= MAX )
    ASSERT( MIN <= b <= MAX )
    ASSERT( MIN <= c <= MAX )
    #return [ a, oper, b, '=', c ]
    return [ getRMBName(a), oper, getRMBName(b), '=', '____元____角' ]  
'''],



['数独', '''\
def generator():
    GRID = 3
    ret = []
    board = Sudoku( GRID )
    board.solve()
    for i in range(GRID**2):
        for j in range(GRID**2):
            v = board.masked_grid[i*GRID**2+j]
            #v = board.solution[i*GRID**2+j]
            ret.append( ' ' if v == '_' else v  )
        ret.append('EOL') 
    return ret
'''],

['加减乘法表', '''\
oper='*'
line=1
def generator():
    global line, oper
    if line > 10:
        STOP()
    ret = []
    for i in range(line, 10+1):
        if oper == '*':
            s = '%d%s%d=%d'% (line, oper, i, line * i )
        elif oper == '+':
            s = '%d%s%d=%d'% (line, oper, i, line + i )
        elif oper == '-':
            s = '%d%s%d=%d'% (i, oper, line, i - line )
        ret.append( s )
    line += 1
    return ret
'''],


['12/24时间制式转换', '''\
def getTimeName(hour, minute, format_24h):
    if format_24h:
        r = '%d时'% hour
    else:
        if hour <= 12:
            r = '上午%d时'% hour
        else:
            r = '下午%d时'% (hour-12)
    if minute == 0:
        pass
    elif minute == 30:
        r += '半'
    return r

def generator():
    global getTimeName
    hour = randint(0,23)
    minute = choice([0,30])
    name = '%d:%02d'% (hour, minute)
    return [ name, getTimeName(hour,minute,False), getTimeName(hour,minute,True) ]
'''],

['四则混合运算（3个数）', '''\
def generator():
    MIN, MAX = 0, 10000
    a = randint(MIN, 99)
    b = randint(MIN, 99)
    c = randint(MIN, MAX)
    oper1 = choice( '*/' ) 
    oper2 = choice( '+-' ) 
    inv = bool(random() > 0.5)
    ASSERT( a < 100 )
    ASSERT( b < 100 )
    if oper1 == '*':
        ab = a * b
    else:
        ASSERT( b > 0 )
        ab = a / b
        ASSERT( ab * b == a )
    ASSERT( 0 <= ab <= MAX )
    if oper2 == '+':
        d = ab + c 
    elif inv:
        d = c - ab 
    else:
        d = ab - c
    ASSERT( 0 <= d <= MAX )
    if inv:
        return [ c, oper2, a, oper1, b, '=', d ]
    else:
        return [ a, oper1, b, oper2, c, '=', d ]
'''],


]

CONFIGS_DICT = {}
for k,v in CONFIGS_LIST:
    CONFIGS_DICT[k] = v

###############################################################################

class AssertError(Exception):
    pass

class StopError(Exception):
    pass


def ASSERT(condition):
    if not condition:
        raise AssertError()

def STOP(message=''):
    raise StopError(message)


def load_cn_words(fname):
    ret=[]
    if not os.path.isfile(fname):
        STOP('文件 %s 不存在'% fname)
    for l in open(fname,'r').read().decode(encoding='utf8').splitlines():
        l = l.split('#')[0].strip()
        if not l or l == '\ufeff':
            continue
        for w in l.split(' '):
            if not w or w.startswith('~'):
                continue
            if w in ret:
                continue
            ret.append(w)
    return ret

def getRMBName(m): 
    if m < 1.0:
        return '%d角'% (10*m) 
    elif m-floor(m):
        return '%d元%d角'% (floor(m), 10*m-10*floor(m)) 
    else:
        return '%d元'% (floor(m)) 



class MainDialog(MyDialog):

    def __init__(self, *args, **kwds):
        MyDialog.__init__( self, *args, **kwds )
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.init_text_ctrl_rules()
        self.button_generate.Enable(False)
        self.button_copy_result.Enable(False)
        self.combo_box_type.SetValue('请选择出题类型...')
        self.combo_box_type.AppendItems([c[0] for c in CONFIGS_LIST]) 
        self.text_ctrl_number.SetValue('100')
        self.clrAllResult()

    def OnClose(self, event):
        self.Destroy()
        event.Skip()
        
    def OnSelectType(self, event):
        self.info('')
        tp = self.combo_box_type.GetValue()
        if CONFIGS_DICT.has_key(tp):
            self.text_ctrl_rules.SetValue( CONFIGS_DICT[tp] )
            self.button_generate.Enable(True)
        else:
            self.button_generate.Enable(False)
        event.Skip()

    def clrAllResult( self ):
        self.grid_result.ClearGrid()
        lines = self.grid_result.GetNumberRows()
        if lines:
            self.grid_result.DeleteRows(numRows=lines)

    def addResult( self, result ):
        if self.grid_result.AppendRows():
            line = self.grid_result.GetNumberRows()
            index = 0
            for item in result:
                if isinstance(item, unicode) and item == 'EOL':
                    if self.grid_result.AppendRows():
                        line += 1
                        index = 0
                    else:
                        return 
                else:
                    self.grid_result.SetCellValue( line-1, index, unicode(item) )
                    index += 1
        else:
            return
     
    def info( self, info, info_type=wx.ICON_WARNING ):
        if info:
            self.window_info.ShowMessage(info, info_type)
        else:
            self.window_info.Dismiss()
 
    def OnGenerate(self, event):
        self.info('')
        rules = self.text_ctrl_rules.GetValue()
        try:
            num = int(self.text_ctrl_number.GetValue())
            if num <= 0 or num > 10000:
                raise Exception
        except:
            self.info('出题数量错误', wx.ICON_ERROR)
            return
        counter = 0
        try:
            code = compile(rules, '', 'exec')
            exec( code )
            generator
        except Exception as e:
            self.info(unicode(e), wx.ICON_ERROR)
            return
        self.clrAllResult()
        t0 = time.time()
        while counter < num:
            try:
                result = generator()
                counter += 1 
                self.addResult( result )
            except AssertError:
                pass
            except StopError as e:
                self.info(unicode(e), wx.ICON_ERROR)
                break
            except Exception as e:
                self.info(unicode(e))
                return
        t1 = time.time()
        print( 'time elapsed: %.1f seconds'% (t1-t0) )
        self.button_copy_result.Enable(True)
        event.Skip()

    def OnCopyResult(self, event):
        self.info('')
        lines = self.grid_result.GetNumberRows()
        if lines:
            ret = []
            for l in range(lines):
                items = [self.grid_result.GetCellValue( l, c ) \
                         for c in range(26)]
                cp = '\t'.join(items).rstrip('\t')
                print cp
                ret.append( cp )
            copy = '\r\n'.join(ret)
            import pyperclip
            pyperclip.copy( copy )
        event.Skip()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, ABOUT_INFO, '关于', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
 
    def init_text_ctrl_rules(self):
        ctrl = self.text_ctrl_rules
        faces = { 'times': 'Courier New',
                  'mono' : 'Courier New',
                  'helv' : 'Courier New',
                  'other': 'Courier New',
                  'size' : 12,
                  'size2': 10,
                }
        ctrl.SetLexer(wx.stc.STC_LEX_PYTHON)
        ctrl.SetKeyWords(0, " ".join(keyword.kwlist))
        ctrl.SetProperty("tab.timmy.whinge.level", "1")
        ctrl.SetMargins(0,0)
        ctrl.SetViewWhiteSpace(False)
        ctrl.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        ctrl.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        ctrl.StyleClearAll()
        ctrl.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        ctrl.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")
        ctrl.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        ctrl.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
        ctrl.SetCaretForeground("BLACK")
        ctrl.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        ctrl.SetMarginWidth(1, 40)
    

    def OnUpdateUI(self, evt):
        ctrl = self.text_ctrl_rules
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = ctrl.GetCurrentPos()

        if caretPos > 0:
            charBefore = ctrl.GetCharAt(caretPos - 1)
            styleBefore = ctrl.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and (32 < charBefore < 128):
            if chr(charBefore) in "[]{}()" and styleBefore == wx.stc.STC_P_OPERATOR:
                braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = ctrl.GetCharAt(caretPos)
            styleAfter = ctrl.GetStyleAt(caretPos)
            if charAfter and (32 < charAfter < 128):
                if chr(charAfter) in "[]{}()" and styleAfter == wx.stc.STC_P_OPERATOR:
                    braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = ctrl.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            ctrl.BraceBadLight(braceAtCaret)
        else:
            ctrl.BraceHighlight(braceAtCaret, braceOpposite)



if __name__ == "__main__":
    gettext.install("app")
    app = wx.App(0)
    app.SetAppName( 'ExerciseGeneratorApp' )
    dialog_1 = MainDialog(None, wx.ID_ANY, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
