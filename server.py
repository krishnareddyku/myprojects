from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Set response status code
        self.send_response(200)
        
        # Set response headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

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
        self.wfile.write(response_message.encode('utf-8'))

if __name__ == '__main__':
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
