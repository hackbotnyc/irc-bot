import socket
import string
import mraa
import Queue
import threading
import urllib
import urllib2

LEFT_MOTOR_PORT = 12
RIGHT_MOTOR_PORT = 13

left_motor = None
right_motor = None

# init all the things
left_motor = mraa.Gpio(LEFT_MOTOR_PORT)
right_motor = mraa.Gpio(RIGHT_MOTOR_PORT)

left_motor.dir(mraa.DIR_OUT)
right_motor.dir(mraa.DIR_OUT)

def set_left_motor(on):
    if on:
        left_motor.write(1)
    else:
        left_motor.write(0)

def set_right_motor(on):
    if on:
        right_motor.write(1)
    else:
        right_motor.write(0)

def run():
    readbuffer = ""

    s = socket.socket()
    s.connect(("irc.esper.net", 6667))
    s.send("NICK hackbot\r\n")
    s.send("USER hackbot irc.esper.net bla :HackBot\r\n")

    while True:
        readbuffer = readbuffer + s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = string.rstrip(line).split(line)
            print line[0]
            l = line[0].split(" ")
            if l[0] == "PING":
                print "pong"
                s.send("PONG %s\r\n" % l[1])
            if len(l) >= 4:
                l.remove(l[0])
                l.remove(l[0])
                l.remove(l[0])
                l[0] = l[0].replace(":", "")
                args = l

                if args[0] == "End":
                    s.send("JOIN #hackcooper\r\n")
                elif args[0] == "!move":
                    set_left_motor(args[1] == "on")
                elif args[0] == "!forward":
                    set_left_motor(True)
                    set_right_motor(True)
                elif args[0] == "!left":
                    set_left_motor(False)
                    set_right_motor(True)
                elif args[0] == "!right":
                    set_left_motor(True)
                    set_right_motor(False)
                elif args[0] == "!break":
                    set_left_motor(False)
                    set_right_motor(False)

# reset both motors on startup
set_left_motor(False)
set_right_motor(False)

run()
