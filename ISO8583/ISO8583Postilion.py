"""

(C) Copyright 2009-2021 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__ =  'Igor Vitorio Custodio <igorvc@vulcanno.com.br>'
__version__=  '2.0.1'
__licence__ = 'GPL V3'


from ISO8583 import *
from ISOErrors import *
import struct


class ISO8583Postilion(ISO8583):
    """Class to work with ISO8583Postilion packages.
    Used to create, change, send, receive, parse or work with ISO8583 Package version Postilion.
    It's 100% Python :)
    Enjoy it!
    Thanks to: Vulcanno IT Solutions <http://www.vulcanno.com.br>
    Licence: GPL Version 3
    More information: http://code.google.com/p/iso8583py/

    Example:
        from ISO8583 import *
        from ISO8583.ISO8583Postilion import ISO8583Postilion
        from ISO8583.ISOErrors import *
        
        iso = ISO8583Postilion()
        try:
            iso.setMTI('0800')
            iso.setBit(2,2)
            iso.setBit(4,4)
            iso.setBit(12,12)
            iso.setBit(21,21)
            iso.setBit(17,17)
            iso.setBit(49,986)
            iso.setBit(99,99)
        except ValueToLarge, e:
                print ('Value too large :( %s' % e)
        except InvalidMTI, i:
                print ('This MTI is wrong :( %s' % i)
                
        print ('The Message Type Indication is = %s' %iso.getMTI()) 
        
        print ('The Bitmap is = %s' %iso.getBitmap()) 
        iso.showIsoBits();
        print ('This is the ISO8583Postilion complete package %s' % iso.getRawIso())
        print ('This is the ISO8583Postilion complete package to sent over the TCPIP network %s' % iso.getNetworkISO())
    
"""
       
    ################################################################################################

   
    