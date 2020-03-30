import socket
import threading
import queue

inbound_que = queue.Queue()
outbound_que = queue.Queue()

def accept_connection( sock ):

    global receive_thread, send_thread

    try:
        new_sock = sock.accept()[ 0 ]
        clients[new_sock] = ""
        receive_thread = threading.Thread( target=receive_message, args=(new_sock,) )
        receive_thread.start()
        send_thread = threading.Thread( target=send_message_from_que, args=(new_sock,) )
        send_thread.start()
        print("acepted_connection")
    except Exception as e:
        print("Error: Could not connect, ", e)


def receive_message( sock ):

    message_len = 0

    while True:
        # get the message length
        try:
            # receive the first couple of bytes for our message len
            data = sock.recv( 2 )
            message_len = int.from_bytes( data, 'big' )
        except Exception as e:
            print( "Bad receive, ", e )

        try:
            message = sock.recv( message_len ).decode( "utf-8" )
            #send_message(sock, message)
            inbound_que.put ( message, False )
            #print("message recived, ", message_len, message)
        except Exception as e:
            print( "Bad receive, ", e )

def que_message( message, sock ):

    global send_thread

    outbound_que.put( message, False )

    #if send_thread is None or not send_thread.is_alive():
    #    send_thread = threading.Thread( target=send_message_from_que, args=(sock,) )
    #    send_thread.start()

def send_message( sock, message ):

    message_length = len( message )

    len_bytes = message_length.to_bytes(2, 'big')
    message_bytes = message.encode()

    try:
        sock.send( len_bytes + message_bytes )
        print("sent")
    except Exception as e:
        print( "Bad send..., ", e )

def send_message_from_que( sock ):

    while True:
        while not outbound_que.empty():
            message = outbound_que.get(False)
            send_message( sock, message )

if __name__ == "__main__":

    clients = {}
    clients_max = 12
    running = True

    socket_inst = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    socket_inst.bind( ("127.0.0.1", 8333) )
    socket_inst.listen( clients_max )

    thread_lock = threading.Lock()

    receive_thread = None # threading.Thread( target=receive_message, args=(socket_inst,) )
    accept_thread = threading.Thread( target=accept_connection, args=(socket_inst,) )
    send_thread = None # threading.Thread( target=send_message, args=(socket_inst,) )

    accept_thread.start()

    while running:

        # streat from inpbound
        #if not inbound_que.empty():
        #    send_message( list(clients)[0], inbound_que.get(False) )

        # que message method
        if not inbound_que.empty():
            que_message( inbound_que.get(False), list(clients)[0] )

        pass