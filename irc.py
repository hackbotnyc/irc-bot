import socket
import string

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
                    print "OMG MOVE FORWARD"

run()
