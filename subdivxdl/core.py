
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
def mysend(sock, sdata, expected, verbose):
    buff_size = 4096 # 4 KiB
    if verbose >= 3: log.p.cout(repr(sdata))
    sock.sendall(sdata)

    fragments = []
    while True:
        try:
            chunk = sock.recv(buff_size)
            if verbose >= 3: log.p.cin(repr(chunk))
            fragments.append(chunk)
            if chunk[-4:] == b'\r\n\r\n': break
        except socket.timeout:
            log.p.info("Timeout")
            break
        # except:
        #     log.p.fail("Something else went wrong")
        #     break

    full_text = b''.join(fragments)
    #print(repr(full_text))
    #print(full_text.decode("iso-8859-1"))

    print("FIN")
    #print(rdata.decode("utf-8"))

    # if rdata.decode("utf-8")[:3] != expected:
    #     log.p.fail(expected+' reply not received from server')

def send(verbose):
    host = 'www.subdivx.com'
    bhost = host.encode('utf-8')
    port = 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(5)

    # User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    petition =  b'GET / HTTP/1.1\r\n' \
                b'Host: www.subdivx.com\r\n' \
                b'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0\r\n' \
                b'Accept-Language: en-us\r\n' \
                b'Connection: Keep-Alive\r\n\r\n'
                # b'Accept-Encoding: gzip, deflate\r\n\r\n'

    mysend(sock, petition, '200', verbose)

    sock.close()

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
    send(verbose)

    # --- Exit -----------------------------------------------------------------
    if verbose >= 1: log.p.exit("end of the execution")
