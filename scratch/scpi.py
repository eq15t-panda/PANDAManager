import os
import time

def scpi_write(fd, cmd: str) -> None:
    os.write(fd, (cmd + "\n").encode())

def scpi_readline(fd) -> str:
    data = b""
    while True:
        c = os.read(fd, 1)
        if c == b"\n":
            break
        if c == b"":
            raise RuntimeError("Timeout / empty read from SCPI device")
        data += c
    return data.decode().strip()

def scpi_query(fd, cmd: str) -> str:
    scpi_write(fd, cmd)
    return scpi_readline(fd)

def read_exact(fd, nbytes: int) -> bytes:
    buf = b""
    while len(buf) < nbytes:
        chunk = os.read(fd, nbytes - len(buf))
        if not chunk:
            raise RuntimeError("Unexpected EOF while reading from SCPI device")
        buf += chunk
    return buf

def read_block(fd) -> bytes:
    '''
    Read a SCPI definite-length binary block: #<n><len><data>
    Consume one trailing newline if present.
    '''
    first = read_exact(fd, 1)
    if first != b"#":
        raise RuntimeError(f"Invalid binary block header start: {first!r}")
    n_digits = int(read_exact(fd, 1).decode())
    length = int(read_exact(fd, n_digits).decode())
    payload = read_exact(fd, length)
    try:
        tail = os.read(fd, 1)
        if tail not in (b"", b"\n"):
            pass
    except Exception:
        pass
    return payload
