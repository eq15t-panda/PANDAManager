from os import write


def write(cmd, fd):
    write(fd, (cmd + "\n").encode())