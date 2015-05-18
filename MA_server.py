import socket
from rakutenma import RakutenMA

def start_function_server(f, port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('localhost', port))
    serv.listen(0)
    print 'Server started'
    while True:
        conn, addr = serv.accept()
        buf = conn.recv(2000).decode('utf-8')
        print 'Received input\n' + buf + 'from ' + repr(addr)
        try:
            res = f(buf)
            print 'Sending result\n' + res + '\n'
            conn.send(res.encode('utf-8'))
        except:
            print 'Error: Unable to compute result'
        conn.close()

def create_tokenizer():
    rma = RakutenMA()
    rma.load('model_ja.json')
    rma.hash_func = rma.create_hash_func(15)
    return rma.tokenize

def decode_result(res):
    return repr(res).decode('unicode-escape')

def split_only(res):
    return [word for [word, tag] in res]

def split_sentence(s, tok):
    return decode_result(split_only(tok(s)))

def tag_sentence(s, tok):
    return decode_result(tok(s))

def main():
    tok = create_tokenizer()
    start_function_server(lambda s: tag_sentence(s, tok), 56565)

if __name__ == '__main__':
    main()
