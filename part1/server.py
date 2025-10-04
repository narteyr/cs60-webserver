#Open a TCP socket
   # Bind to a port of your choosing
   # Loop forever
   #     Accept a connection to your socket (returns socket for the client that connected)
   #     Read the data from client socket, expecting GET /<filename>
   #     if file found
   #         Open file with filename and read contents into a buffer of bytes
   #         Send via the client socket
   #            Create HTTP OK message headers (see slide 102 from class, just the status line will suffice)
   #             Create HTTP OK message headers (see slide 102 from class, just the status line will suffice)
   #            // chunk buffer where each size(chunk + header) < max TCP packet size 
    #            // (or find a command to handle chunking for you)
    #            Create a message for each chunk of the buffer
    #                    Concatenate HTTP OK header and chunk bytes
   #                     Append "\r\n" (carriage return and new line) to the end
    #                    Send this appended message out the client socket
  #          else
   #         Send "HTTP/1.1 404 Not Found\r\n\r\n <html><head></head><body><h1>404 Not Found</h1></body></html>\r\n" message
   #     Close client socket

from enum import Enum
import socket
import os

class StatusCode(Enum):
    NOT_FOUND = 404
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500


#define host and ip address
HOST = '0.0.0.0'
PORT = 9091

#create TCP socket listening on IP ADDRESS AND PORT
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))

methods = set(["GET", "POST", "PUT", "DELETE"])
MIN_PARAMS = 3

#listen for connections
server_socket.listen()
print(f"Server is listening for connections at port:{PORT}....")

try:
    client_socket, addr = server_socket.accept() #accepts and returns a new client socket
    print(f"Connected by {addr}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        request = data.decode()
        request_params = request.split(" ")

        # validate the user's http request
        if len(request_params) != MIN_PARAMS and request_params[0] not in methods:
            error_message: str = f"HTTP/1.1 {StatusCode.BAD_REQUEST.value} {StatusCode.BAD_REQUEST.name}\r\n\r\n"
            client_socket.sendall(error_message.encode())
            break

        if request_params[0] in methods and request_params[0] == "GET":
            file_path: str = request_params[1]
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = request_params[1].lstrip("/")
            file_path = os.path.join(base_dir, file_path)
            try:
                with open(file_path, "r") as fp:
                    data = fp.read()
                    client_socket.sendall(data.encode())
            except FileNotFoundError:
                    error_message: str = "HTTP/1.1 404 Not Found\r\n\r\n <html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
                    client_socket.sendall(error_message.encode())
                    break
        
        print(f"Received: {data.decode()}\n")
        client_socket.sendall(b"Message received: " + data)

except Exception as e:
    print(f"Status Code: {StatusCode.INTERNAL_SERVER_ERROR.value}, error: {e}")
    server_socket.close()
finally:
    client_socket.close()
    server_socket.close()