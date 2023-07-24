from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            # Open the static file requested
            filepath = os.getcwd() + self.path
            with open(filepath, 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        # Get the content length of the POST data
        content_length = int(self.headers['Content-Length'])

        # Read the POST data from the request
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Parse the POST data to extract the value of 'data_input' field from the form
        form_data = cgi.parse_qs(post_data)
        data_input_value = form_data.get('data_input', [''])[0]

        # Process the data (you can do any required processing here)
        print("Received data from browser:", data_input_value)

        # Send a response back to the browser
        response_message = f"Received data: {data_input_value}"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))

def run_server():
    host = 'localhost'
    port = 8000

    # Create and start the HTTP server
    server = HTTPServer((host, port), MyHTTPRequestHandler)
    print(f"Server started on {host}:{port}")

    try:
        # Wait forever for incoming HTTP requests
        server.serve_forever()
    except KeyboardInterrupt:
        # Shut down the server on Ctrl+C
        server.shutdown()

if __name__ == '__main__':
    run_server()
