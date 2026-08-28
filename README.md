# Caching Web Proxy Server

A basic caching web proxy server developed in Python as part of a computer networking course lab. The project demonstrates socket programming, HTTP communication, client-server architecture, and web caching.

## Features

* Accepts client connections using TCP sockets
* Processes HTTP GET requests
* Connects to remote web servers over port 80
* Forwards HTTP responses from web servers to the client
* Stores retrieved web content in a local cache
* Serves previously requested content directly from the cache
* Handles raw response data, including HTML and image content
* Returns a basic `404 Not Found` response when a request cannot be completed

## Concepts Demonstrated

* TCP socket programming
* HTTP requests and responses
* Client-server architecture
* Proxy servers
* Web caching
* Binary file handling
* Basic error handling

## Technologies

* Python
* TCP/IP
* HTTP
* Python Socket API

## Testing

A webpage can be requested through the proxy by entering a URL in the following format:

```text
http://localhost:8888/example.com
```

When content is requested for the first time, the proxy retrieves it from the remote web server and stores the response locally.

The console will display:

```text
Received from web server and saved to cache
```

Requesting the same resource again allows the proxy to serve the locally cached response:

```text
Read from cache
```

## How It Works

1. The proxy creates a TCP socket and listens on port `8888`.
2. A client connects to the proxy and sends an HTTP request.
3. The proxy extracts the requested destination from the request.
4. It checks whether the requested content already exists in the local cache.
5. If cached, the stored response is returned directly to the client.
6. If not cached, the proxy connects to the destination web server on port `80`.
7. The proxy sends an HTTP GET request to the web server.
8. The returned response is forwarded to the client and saved to the cache for future requests.

## Limitations

This project implements a simplified HTTP proxy for educational purposes and is not intended to function as a production web proxy.

* Supports basic HTTP traffic over port 80
* Does not implement HTTPS tunneling
* Some modern websites may redirect HTTP requests to HTTPS
* Relative resource requests may not preserve the original destination hostname, which can prevent some images or other page resources from loading
* Handles one client connection at a time

## About

This project was completed as a computer networking course lab to gain hands-on experience with TCP socket programming, HTTP communication, proxy servers, and web caching.
