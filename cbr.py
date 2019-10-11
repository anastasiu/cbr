# -*- coding: utf-8 -*-
#----------------------------------------
# Author: Anastasiu Aleksandr 
# Email:  anastasiu-a@ya.ru
# Date:   November 25, 2018
#----------------------------------------
import sys
from zeep import Client
from datetime import datetime, timedelta


def fCbrGetCursOnDate(dt,vchCode,getHdr):
    """function Get Data From WebService"""
    rs = ''
    dstHdr = ['Date', 'Vname', 'Vnom', 'Vcurs', 'Vcode', 'VchCode']
    try:
        if getHdr:
            rs = ';'.join(dstHdr)
        else:
            clt = Client("http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL").service.GetCursOnDate(dt)
            for cl in clt['_value_1']['_value_1']:
                 if str(cl['ValuteCursOnDate']['VchCode']).strip() in vchCode:
                       rs += str(dt.date()) + ';'
                       for dh in dstHdr[1:]: rs += str(cl['ValuteCursOnDate'][dh]).strip() + ';'
                       rs = rs[:-1] +'\n'
            rs = rs[:-1]
    except:
        print('Err_desc: ' + str(sys.exc_info()[1]))
    return rs


def fCheckDate(dt):
    """function for Check Date"""
    rs = False
    try:
        rs = datetime.strptime(dt, '%d.%m.%Y')
    except:
        pass
    return rs


def fPrintEx():
    """function Print Example"""
    print('*******************************************************************************')
    print('Скрипт запускается только с обязательными параметрами, вот так: \n'
           + 'python3 cbr.py dtstart:=20.01.2018 vchcode:=EUR,USD,JPY \n'
           + 'или с расширенными, так: \n'
           + 'python3 cbr.py dtstart:=20.01.2018 dtend:=25.01.2018 vchcode:=EUR,USD,JPY,CAD'
         )
    print('*******************************************************************************')


if __name__ == "__main__":

    try:
        dctArgs = dict() #Словарь аргументов переданных при запуске скрипта

        if len(sys.argv) > 1:
            for arg in sys.argv:
                if arg.find(':=') > 0:
                   dctArgs[arg.split(':=')[0].strip()] = arg.split(':=')[1].strip()

            if 'dtstart' not in dctArgs:
                fPrintEx()
                sys.exit('Не найден обязательный параметр dtstart')

            dctArgs['dtstart'] = fCheckDate(dctArgs['dtstart'])
            if not dctArgs['dtstart']:
                fPrintEx()
                sys.exit('Параметр dtstart не соответсвует формату даты: 20.02.2018')

            if 'dtend' not in dctArgs:
                dctArgs['dtend'] = dctArgs['dtstart']
            else:
                dctArgs['dtend'] = fCheckDate(dctArgs['dtend'])
                if not dctArgs['dtend']:
                    fPrintEx()
                    sys.exit('Параметр dtend не соответсвует формату даты: 20.02.2018')

            if 'vchcode' not in dctArgs:
                fPrintEx()
                sys.exit('Не найден обязательный параметр vchcode')

            vchcode = list(dctArgs['vchcode'].upper().split(','))
            dt = dctArgs['dtstart']
            rs = ''

            while dt <= dctArgs['dtend']:
                rs += '\n' + fCbrGetCursOnDate(dt, vchcode, False)
                dt += timedelta(days=1)

            if len(rs.split()) > 0:
                rs = fCbrGetCursOnDate('', '', True) + rs
                if 'dout' in dctArgs:
                    with open(dctArgs['dout'], mode="w", encoding="utf8") as dout:
                        dout.write(rs)
                else:
                    print(rs)
        else:
            fPrintEx()
    except:
        print('Err_desc: ' + str(sys.exc_info()[1]))
