import os
import socket
import time
import RPi as gpio
import serial
import sys
import smbus

bus = smbus.SMBus(1)
address = 0x04
cmd = 255

# def writeNumber(value):
#     bus.write_byte(address, value)
#     #bus.write_byte_data(address, 0, value)
#     return -1

# def readNumber():
#     number = bus.read_byte(address)
#     # number = bus.read_byte_data(address, 1)
#     return number

# while True:
#     var = input("Enter number")
#     if not var:
#         continue

#     writeNumber(var)
#     print 'RPI: Hi Arduino, I sent you ', var
#     # sleep one second
#     time.sleep(1)

#     number = readNumber()
#     print 'Arduino: Hey RPI, I received a digit ', number

socket_path = '/tmp/uv4l.socket'

try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)

print 'socket_path: %s' % socket_path
s.bind(socket_path)
s.listen(1)

ser = serial.Serial('/dev/ttyACM0',9600)
time.sleep(2) #arduino usb serial reset allowance HACK

while True:
    print 'awaiting connection...'
    connection, client_address = s.accept()
    print 'client_address %s' % client_address
    try:
        print 'established connection with', client_address

        while True:
            data = connection.recv(16)
            #data = int(data)
            print 'received message"%s"' % data
            #print type(data)
            print data[2:4]
            time.sleep(0.01)
            
            if data[2:4] != 'do':
            #    print 'echo data to client'
            #    connection.sendall(data)
                ser.write(data)
                #bus.write_byte_data(address, cmd, data)
            elif data[2:4] == 'do':
                print 'device orientation'
            else:
                print 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()

