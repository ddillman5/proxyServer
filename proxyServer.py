from socket import *
import sys
# if len(sys.argv) <= 1:
#     print('Usage: "python ProxyServer.py server_ip"\n[server_ip : It is in the IP Address Of Proxy Server')
#     sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM) # Create TCP socket
tcpSerSock.bind(("", 8888)) # Bind the socket
tcpSerSock.listen(1) # Begin listening on port 8888

while True:

    # Start receiving data from the client
    print("Ready to serve...")

    tcpCliSock, addr = tcpSerSock.accept() # Accept the connection
    print("Received a connection from:", addr) # Print connection address

    message = tcpCliSock.recv(4096).decode() # 'message' holds HTTP request

    print(message) # Print HTTP request

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)

    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check whether the file exists in the cache
        # Open and read the file, then set fileExist to true
        f = open(filetouse[1:], "rb")
        outputdata = f.read()
        fileExist = "true"

        # ProxyServer finds a cache hit and sends the cached response to the browser
        tcpCliSock.sendall(outputdata)

        f.close()
        print("Read from cache")

    # Error handling for file not found in cache
    except IOError:

        if fileExist == "false":

            # Create a socket on the proxy server
            # c socket lets proxy server communicate to web page
            c = socket(AF_INET, SOCK_STREAM)

            hostn = filename.replace("www.", "", 1)
            print(hostn)

            try:
                # Connect to the socket on port 80
                c.connect((hostn, 80))

                # Create a temporary file on this socket and request the page
                fileobj = c.makefile("rwb", buffering=0)

                request = (
                        "GET http://" + filename + " HTTP/1.0\r\n"
                         "Host: " + hostn + "\r\n"
                         "Connection: close\r\n"
                         "\r\n"
                )

                fileobj.write(request.encode()) # Write HTTP request into socket

                # Read the response into buffer
                buffer = fileobj.read()

                # Create a new file in the cache for the requested file.
                # Also send the response to the client.
                tmpFile = open("./" + filename, "wb") # Create and add file to cache
                tmpFile.write(buffer) # Write data to our tmpFile
                tcpCliSock.sendall(buffer) # Send response to the clients browser
                tmpFile.close() # Close the tmpFile

                fileobj.close()
                c.close()

                print("Received from web server and saved to cache")

            except:
                print("Illegal request")

                # Display a 404 error in the case that the proxy cannot obtain the webpage
                tcpCliSock.sendall(
                    (
                        "HTTP/1.0 404 Not Found\r\n"
                        "Content-Type: text/html\r\n"
                        "Connection: close\r\n"
                        "\r\n"
                        "<html><body><h1>404 Not Found</h1></body></html>"
                    ).encode()
                )

        else:
            # Fallback to display 404 error if proxy server cannot provide the requested URL
            tcpCliSock.sendall(
            (
                "HTTP/1.0 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<html><body><h1>404 Not Found</h1></body></html>"
            ).encode()
        )

    # Close the client socket
    tcpCliSock.close()

# Close the server socket
tcpSerSock.close()