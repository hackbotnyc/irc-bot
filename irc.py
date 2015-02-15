import socket
import string

readbuffer = ""

s = socket.socket()
s.connect(("irc.esper.net", 6667))
s.send("NICK hackbot_____\r\n")
s.send("USER hackbot irc.esper.net bla :HackBot\r\n")

while True:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = string.rstrip(line).split(line)
        l = line[0].split(" ")
        print line
        if l[0] == "PING":
            print "ping"
            s.send("PONG %s\r\n" % l[1])
        if len(l) > 4:
            if l[3] == ":End":
                print "joining..."
                s.send("JOIN hawkfalcon")
