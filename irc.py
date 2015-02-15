import socket
import string

def run():
    readbuffer = ""

    s = socket.socket()
    s.connect(("irc.esper.net", 6667))
    s.send("NICK hackbot_\r\n")
    s.send("USER hackbot irc.esper.net bla :HackBot\r\n")

    while True:
        readbuffer = readbuffer + s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = string.rstrip(line).split(line)
            l = line[0].split(" ")
            print line[0]
            if l[0] == "PING":
                s.send("PONG %s\r\n" % l[1])
            if len(l) > 4:
                if l[3] == ":End":
                    s.send("JOIN #hackcooper\r\n")

run()
