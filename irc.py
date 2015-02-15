import socket
import string
import mraa
import urllib2

LEFT_AUDIO_PORT = 5
RIGHT_AUDIO_PORT = 6

LEFT_MOTOR_PORT = 12
RIGHT_MOTOR_PORT = 13

left_audio = None
right_audio = None

left_motor = None
right_motor = None

# init all the things
left_motor = mraa.Gpio(LEFT_MOTOR_PORT)
right_motor = mraa.Gpio(RIGHT_MOTOR_PORT)

left_audio = mraa.Pwm(LEFT_AUDIO_PORT)
right_audio = mraa.Pwm(RIGHT_AUDIO_PORT)

left_audio.enable(True)
right_audio.enable(True)

left_motor.dir(mraa.DIR_OUT)
right_motor.dir(mraa.DIR_OUT)

left_audio_buffer = []
right_audio_buffer = []

def push_audio(left=0, right=0):
    left_audio_buffer.append(left)
    right_audio_buffer.append(right)

def step_audio():
    if len(left_audio_buffer) > 0:
        left_audio.write(left_audio_buffer.pop(0))
    if len(right_audio_buffer) > 0:
        right_audio.write(right_audio_buffer.pop(0))

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
        step_audio()
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
                elif args[0] == "!say":
                    args.remove(args[0])
                    #values = {'accept': 'audio%2Fwav', 'text': args.join(" ")}
                    #headers = { 'Authorization': 'Basic YjU1Y2VlYWYtZjc0ZS00YTJhLWFkMjYtZGUzMWI5MDA3ZGQwOlJiYk5SYWtZVDA2Qg==' }
                    #data = urllib.urlencode(values)
                    #request = urllib2.Request("https://stream.watsonplatform.net/text-to-speech-beta/api/v1/synthesize", data, headers)
                    #response = urllib2.urlopen(request)
                    #stuff = response.read()
                    print args

# reset both motors on startup
set_left_motor(False)
set_right_motor(False)

run()
