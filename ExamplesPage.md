# Introduction #

This project has a lot of examples inside the "examples" directory.

This page, want to give some information about what you will find in each example.


# ISO8583 Echo Client/Server #

This is one of the most important examples, because:
  * Use the library :)
  * Build a package
  * Send it by socket
  * Receive it by Socket
  * Redefine a bit specification
  * It's complete!

## Echo ##

In ISO8583 operation, is common to have a protocol to change information and keep the service alive.

This protocol use a package and a transation that have the name "Echo".

In Echo, a Client send a package with MTI 0800 and some bits to the server asking "Hi, Is everything OK?"

If the server is OK, it sends back a package with MTI 0810. So the client can keep walking ...


## Echo Server ##

Is a very simple Socket single-thread server that receive a ISO8583 package, process it, and answer if is everything ok.

This is the code:

```
"""

(C) Copyright 2009 Igor V. Custodio

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


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
from socket import *

# Configure the server
serverIP = "192.168.0.103" 
serverPort = 8583
maxConn = 5
bigEndian = True
#bigEndian = False


# Create a TCP socket
s = socket(AF_INET, SOCK_STREAM)    
# bind it to the server port
s.bind((serverIP, serverPort))   
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)                        


# Run forever
while 1:
	#wait new Client Connection
	connection, address = s.accept() 
	while 1:
		# receive message
		isoStr = connection.recv(2048) 
		if isoStr:
			print ("\nInput ASCII |%s|" % isoStr)
			pack = ISO8583()
			#parse the iso
			try:
				if bigEndian:
					pack.setNetworkISO(isoStr)
				else:
					pack.setNetworkISO(isoStr,False)
			
				v1 = pack.getBitsAndValues()
				for v in v1:
					print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
					
				if pack.getMTI() == '0800':
					print ("\tThat's great !!! The client send a correct message !!!")
				else:
					print ("The client dosen't send the correct message!")	
					break
					
					
			except InvalidIso8583, ii:
				print (ii)
				break
			except:
				print ('Something happened!!!!')
				break
			
			#send answer
			pack.setMTI('0810')
			
			if bigEndian:
				ans = pack.getNetworkISO()
			else:
				ans = pack.getNetworkISO(False)
				
			print ('Sending answer %s' % ans)
			connection.send(ans)
			
		else:
			break
	# close socket		
	connection.close()             
	print ("Closed...")
```

## Echo Client ##

It's a very simple client that connect with Socket and send a ISO8583 package.

```
"""

(C) Copyright 2009 Igor V. Custodio

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


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
import socket
import sys
import time


# Configure the client
serverIP = "192.168.0.103" 
serverPort = 8583
numberEcho = 5
timeBetweenEcho = 5 # in seconds

bigEndian = True
#bigEndian = False

s = None
for res in socket.getaddrinfo(serverIP, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
		s = socket.socket(af, socktype, proto)
    except socket.error, msg:
	s = None
	continue
    try:
		s.connect(sa)
    except socket.error, msg:
	s.close()
	s = None
	continue
    break
if s is None:
    print ('Could not connect :(')
    sys.exit(1)
	
	
	
for req in range(0,numberEcho):
	iso = ISO8583()
	iso.setMTI('0800')
	iso.setBit(3,'300000')	
	iso.setBit(24,'045')	
	iso.setBit(41,'11111111')	
	iso.setBit(42,'222222222222222')	
	iso.setBit(63,'This is a Test Message')
	if bigEndian:
		try:
			message = iso.getNetworkISO() 
			s.send(message)
			print ('Sending ... %s' % message)
			ans = s.recv(2048)
			print ("\nInput ASCII |%s|" % ans)
			isoAns = ISO8583()
			isoAns.setNetworkISO(ans)
			v1 = isoAns.getBitsAndValues()
			for v in v1:
				print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
				
			if isoAns.getMTI() == '0810':
				print ("\tThat's great !!! The server understand my message !!!")
			else:
				print ("The server dosen't understand my message!")
					
		except InvalidIso8583, ii:
			print (ii)
			break	
		

		time.sleep(timeBetweenEcho)
		
	else:
		try:
			message = iso.getNetworkISO(False) 
			s.send(message)
			print ('Sending ... %s' % message)
			ans = s.recv(2048)
			print ("\nInput ASCII |%s|" % ans)
			isoAns = ISO8583()
			isoAns.setNetworkISO(ans,False)
			v1 = isoAns.getBitsAndValues()
			for v in v1:
				print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
					
			if isoAns.getMTI() == '0810':
				print ("\tThat's great !!! The server understand my message !!!")
			else:
				print ("The server dosen't understand my message!")
			
		except InvalidIso8583, ii:
			print (ii)
			break	
		
		time.sleep(timeBetweenEcho)

		
		
print ('Closing...')		
s.close()		
			
```

# Example 1 #

This is a very simple example, that show how to use the library, how to deal with Exceptions etc.

```
"""

(C) Copyright 2009 Igor V. Custodio

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

from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
import traceback

#Clean the shell
import os
os.system(['clear','cls'][os.name == 'nt'])

# get new object
p = ISO8583()
#some string describing the transation type
transation = "200"
print ('Setting transation type to %s' % transation)
p.setTransationType(transation)
# Is the same that:
#p.setMTI(transation)

#Some tests and 
print ('Setting bits')

p.setBit(3,"100000")
p.setBit(4,1200)
p.setBit(7,"1207231505")
p.setBit(11,12)
p.setBit(12,"231505")
p.setBit(13,1207)
p.setBit(32,"01020000000")
p.setBit(40,"002")
p.setBit(41,"98765432")
p.setBit(42,"303500098765432")
p.setBit(49,986)
p.setBit(62,"PP16814995840013560000")
p.setBit(63,"00000105")
try:
	p.setBit(126,"00000000000000105")
except ValueToLarge:
	print ('\t\tSomething happening!!!! The Exception! So, bit 126 is not set!!!!')
	#if want more information ...
	#traceback.print_exc()

#show hex bitmap
print ('Bitmap in HEX')
p.showBitmap()

#Show bits
print ('Bits with values')
p.showIsoBits()

# Show raw ASCII ISO
print ('The package is -> ')
p.showRawIso()

# Getting bits...
print ('\n\n\n------------------------------------------\n')

print ('Getting bits')
try:
	print ('Bit 7 is there? %s' % p.getBit(7))
	print ('Bit 32 is there? %s' % p.getBit(32))
except:
	print ('Something is bad...')
	
# Testing exceptions...	
try:
	print ('Bit 45 is there? %s' % p.getBit(45))
except:
	print ("No, this bit is not there :)")	

try:
	print ('Bit 27 is there? %s' % p.getBit(27))
except BitNotSet, bns:
	print bns	
	

#More exceptions...	
print ('\n\n\n------------------------------------------\n')
print ('Exceptions....')

iso = ISO8583()
try:
	iso.setMTI('0800')
	iso.setBit(2,2)
	iso.setBit(4,4)
	iso.setBit(12,12)
	iso.setBit(21,21)
	iso.setBit(17,17)
	iso.setBit(49,9861) # this bit is wrong ...
	iso.setBit(99,99)
except ValueToLarge, e:
		print ('Value too large :( %s' % e)
except InvalidMTI, i:
		print ('This MTI is wrong :( %s' % i)

```

# Example 2 #

This example want to show how to deal with getters and setters bits.
It shows too how to compare two ISO8583 Objects.

```
"""

(C) Copyright 2009 Igor V. Custodio

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


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *

import traceback

import os
os.system(['clear','cls'][os.name == 'nt'])

# Testing some funcionalities
p2 = ISO8583()
p2.setMTI('0800')
p2.setBit(2,2)
p2.setBit(4,4)
p2.setBit(12,12)
p2.setBit(17,17)
p2.setBit(99,99)

print ('The MTI is = %s' %p2.getMTI()) 
print ('The Bitmap is = %s' %p2.getBitmap()) 

#Showing bits...
p2.showIsoBits();

#Save the ASCII ISO value without size
iso = p2.getRawIso()

print ('\n\n\n------------------------------------------\n')
print ('This is the ISO <%s> that will be interpreted' % iso)

# New ISO
i = ISO8583()
# Set the ASCII
i.setIsoContent(iso)

# Showing that everything is ok
print ('The MTI is = %s' %i.getMTI()) 
print ('The Bitmap is = %s' %i.getBitmap()) 
print ('Show bits inside the package')
i.showIsoBits()

# Using == to compare ISOS's
print ('Compare ISOs ...')
if i == p2:
	print ('They are equivalent!')
	
else:
	print ('The are differente')
	
# More example...	
print ('\n\n\n------------------------------------------\n')	

i3=ISO8583()
i3.setMTI('0800')
i3.setBit(3,'300000')	
i3.setBit(24,'045')	
i3.setBit(41,'11111111')	
i3.setBit(42,'222222222222222')	
i3.setBit(63,'123testing')	

i3.showIsoBits()

print ('This is the pack %s' %i3.getRawIso())	
```

# Example 3 #

This example want to show how enable Debug information.
It shows too how to print ISO8583 bits, type and value of a object.

```
"""

(C) Copyright 2009 Igor V. Custodio

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

from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *

import traceback

import os
os.system(['clear','cls'][os.name == 'nt'])

#Enable Debug Information
# It's print a lot of information ... So only use if you are developping the library!
p2 = ISO8583(debug=True)
p2.setMTI('0800')
p2.setBit(2,2)
p2.setBit(4,4)
p2.setBit(12,12)
p2.setBit(21,21)
p2.setBit(17,17)
p2.setBit(49,986)
p2.setBit(99,99)
print ('MTI = %s' %p2.getMTI()) 
print ('Bitmap = %s' %p2.getBitmap()) 
p2.showIsoBits();


iso = p2.getRawIso()
#Show debug information of the parsing function
print ('\n\n\n------------------------------------------\n')
print ('Parsing ... <%s> ' % iso)


i = ISO8583()
i.setIsoContent(iso)
#Show information ... to compare
print ('MTI = %s' %i.getMTI()) 
print ('Bitmap = %s' %i.getBitmap()) 
print ('Here we have bits')
i.showIsoBits()


print ('This is the bits and values (1)')
v1 = p2.getBitsAndValues()
print ('\n%s\n' %v1)

print ('This is the bits and values (2)')
v2 = i.getBitsAndValues()	
print ('\n%s\n' %v2)

print ('One way of printing the information ...!')
for v in v1:
	print ('Bit %s of type %s has value = %s' % (v['bit'],v['type'],v['value']))


print ('Another way...')
for v in range(0,len(v2)):
	print ('Bit %s of type %s has value = %s' % (v2[v]['bit'],v2[v]['type'],v2[v]['value']))	
```

# Example 4 #

> This example show how to use the redefineBit and adapt the ISO8583 object to any specification.

```
"""

(C) Copyright 2009 Igor V. Custodio

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

from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *

import traceback

import os
os.system(['clear','cls'][os.name == 'nt'])
	

'''
   00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15    0123456789012345
   -----------------------------------------------    ----------------
00 30 32 31 30 42 32 33 38 30 30 30 31 30 32 43 30    0210B238000102C0
01 38 30 30 34 30 30 30 30 30 30 30 30 30 30 30 30    8004000000000000
02 30 30 30 32 31 30 30 30 30 30 30 30 30 30 30 30    0002100000000000
03 30 30 31 37 30 30 30 31 30 38 31 34 34 36 35 34    0017000108144654
04 36 39 34 32 31 36 31 34 34 36 35 37 30 31 30 38    6942161446570108
05 31 31 30 30 33 30 31 30 30 30 30 30 30 4e 33 39    1100301000000N39
06 39 39 31 35 34 34 34 33 30 33 35 30 30 30 31 39    9915444303500019
07 39 39 31 35 34 34 39 38 36 30 32 30 20 56 61 6c    991544986020 Val
08 6f 72 20 6e 61 6f 20 70 65 72 6d 69 74 69 21 21    ue not allowed!!
09 30 30 39 30 30 30 30 39 35 34 39 32                009000095492

'''
#i2 = ISO8583(debug=True)
i2 = ISO8583()

iso2 = '0210B238000102C080040000000000000002100000000000001700010814465469421614465701081100301000000N399915444303500019991544986020 Value not allowed!!009000095492'
print ('\n\n\n------------------------------------------\n')
print ('This is the ISO <%s> parse it!' % iso2)

i2.setIsoContent(iso2)
print ('Bitmap = %s' %i2.getBitmap()) 
print ('MTI = %s' %i2.getMTI())

print ('Bits')
v3 = i2.getBitsAndValues()
for v in v3:
	print ('(1) Bit %s of type %s and value = %s' % (v['bit'],v['type'],v['value']))
	

# in this case, we need to redefine a bit because default bit 42 is A and in this especification is "N"
# the rest remain, so we use get's to copy original values :)
i2.redefineBit(42, '42', i2.getLargeBitName(42), 'N', i2.getBitLimit(42), i2.getBitValueType(42) )	
print ('\nBit 42 redefined...\n')
	
i3 = ISO8583(iso=iso2)
print ('Bitmap = %s' %i3.getBitmap()) 
print ('MTI = %s' %i3.getMTI())

print ('Bits inside')
v4 = i3.getBitsAndValues()
for v in v4:
	print ('(2) Bit %s of type %s and value = %s' % (v['bit'],v['type'],v['value']))	

```