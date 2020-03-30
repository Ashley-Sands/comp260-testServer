import socket
import threading
import queue

class cli:

    def __init__( self, sock ):

        self.sock = sock
        self.inbound_que = queue.Queue()
        self.outbound_que = queue.Queue()

        #self.send_thread = None
        self.send_thread = threading.Thread( target=self.send_message_from_que, args=( sock,) )
        self.send_thread.start()

        self.receive_thread = threading.Thread( target=self.receive_message, args=( sock,) )
        self.receive_thread.start()

    def receive_message( self, sock ):

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
                #self.send_message(sock, message)
                self.inbound_que.put ( message, block=True )

            except Exception as e:
                print( "Bad receive, ", e )

    def que_message( self, message, sock ):

        self.outbound_que.put( message, block=True)

        #if self.send_thread is None or not self.send_thread.is_alive():
        #    self.send_thread = threading.Thread( target=self.send_message_from_que, args=(sock,) )
        #    self.send_thread.start()

    def send_message( self, sock, message ):

        message_length = len( message )

        len_bytes = message_length.to_bytes(2, 'big')
        message_bytes = message.encode()

        try:
            sock.send( len_bytes + message_bytes )
        except Exception as e:
            print( "Bad send..., ", e )

    def send_message_from_que( self, sock ):

        while True:
            while not self.outbound_que.empty():
                message = self.outbound_que.get(block=True)
                self.send_message( sock, message )

    def process( self ):

        # streat from inpbound
        #if not self.inbound_que.empty():
        #    self.send_message( self.sock, self.inbound_que.get(False) )

        # que message method
        #if not self.inbound_que.empty():
        self.que_message( self.inbound_que.get(block=True), self.sock )
        pass

def accept_connection( sock ):

    while True:
        try:
            new_sock = sock.accept()[ 0 ]
            clients[new_sock] = cli( new_sock )

            thread_lock.acquire()
            clis.append(new_sock)
            thread_lock.release()

            print("acepted_connection")
        except Exception as e:
            print("Error: Could not connect, ", e)


if __name__ == "__main__":

    clients = {}
    clis = []

    clients_max = 50
    running = True

    socket_inst = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    socket_inst.bind( ("127.0.0.1", 8333) )
    socket_inst.listen( clients_max )

    thread_lock = threading.Lock()

    accept_thread = threading.Thread( target=accept_connection, args=(socket_inst,) )
    accept_thread.start()

    while running:
        i = 0

        for c in clis:
            clients[c].process()
            #print(i)
            #i+=1
        pass