
import subdivxdl
from subdivxdl import utils
from subdivxdl import log
from subdivxdl import web

import socket

### EDITABLE VARIABLES #########################################################
TABULAR = " "*8

### AUTOMATIC VARIABLES ########################################################
verbose = 0
# version=open("version.txt").read().replace('\n','')
version="0.0.1"

### FUNCTIONS ##################################################################
def get_html(file, verbose):
    # buff_size = 4096 # 4 KiB
    buff_size = 1024 # 1 KiB
    expected = b'HTTP/1.1 200 OK'
    host = 'www.subdivx.com'
    bhost = host.encode('utf-8')
    port = 80
    fragments = []

    # User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    petition =  b'GET /' + file + b' HTTP/1.1\r\n' \
                b'Host: www.subdivx.com\r\n' \
                b'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0\r\n' \
                b'Accept-Language: en-us\r\n' \
                b'Connection: Keep-Alive\r\n\r\n'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(5)

    if verbose >= 3: log.p.cout(repr(petition) + "\n")
    sock.sendall(petition)

    while True:
        try:
            chunk = sock.recv(buff_size)
            if verbose >= 3: log.p.cin(repr(chunk) + "\n")
            fragments.append(chunk)
            if chunk[-4:] == b'\r\n\r\n': break
        except socket.timeout:
            log.p.info("Timeout")
            break

    if fragments[0][:15] == expected: log.p.ok("HTTP/1.1 200 OK")
    else: log.p.fail("Something went wrong")

    full_text = b''.join(fragments)
    # print(repr(full_text))
    # print(full_text.decode("iso-8859-1"))

    sock.close()
    return full_text

### MAIN #######################################################################
def main():
    # --- Parameters -----------------------------------------------------------
    (options, args) = utils.options_definition()
    # --- verbose
    verbose = 0
    if options.verbose :
        verbose = int(options.verbose)

    # --- CHECK CONFIG ---------------------------------------------------------
    if verbose >= 1: log.p.info("starting subdivxdl v"+version)

    # --- EXECUTION ------------------------------------------------------------
    # get_html(b'', verbose)
    get_html(b'index.php?q=twin%20peaks%20s03e01&accion=5&masdesc=&subtitulos=1&realiza_b=1', verbose)
    # https://regex101.com/r/gU7pz3/1

    # --- Exit -----------------------------------------------------------------
    if verbose >= 1: log.p.exit("end of the execution")
