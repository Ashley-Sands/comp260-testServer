import socket
import time

host = "127.0.0.1"
port = 8333
count = 0

connected = False
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
print(time.time())

# connect
while not connected:
    try:
        sock.connect( (host, port) )
        connected = True
        print("print connection made", sock) # , addr)
    except Exception as e:
        print(e)

while True:
    print("waiting for 1 sec")
    time.sleep(0.1)
    print("pre send")
    try:
        send_time = time.time_ns()

        sock.send( int(4).to_bytes(2, 'big' ) )
        sock.send(b'ping')

        # receive the message skiping over the length.
        data = sock.recv(512).decode("utf-8")

        receive_time = time.time_ns()
        dif = receive_time - send_time
        dif_ms = dif / 1000000

        print("message:", data.encode())
        print(count, "time: ", dif_ms, "ms")

        with open("test_csv.csv", 'a') as f:
            f.write(str(count)+","+str(dif_ms)+",\n")

        count += 1

    except Exception as e:
        print("failed", e)
