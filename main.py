import mimetypes
import pathlib
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from functools import lru_cache


class HttpHandler(BaseHTTPRequestHandler):
    # Initialize Jinja2 environment once
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml']),
        enable_async=False
    )

    # Caching file reading
    @lru_cache(maxsize=128)
    def get_template(self, template_name):
        return self.env.get_template(template_name)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        
        # Save message to data.json
        timestamp = str(datetime.now())
        storage_dir = pathlib.Path('storage')
        storage_dir.mkdir(exist_ok=True)
        data_file = storage_dir / 'data.json'
        
        try:
            messages = {}
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
            
            messages[timestamp] = {
                "username": data_dict.get("username", ""),
                "message": data_dict.get("message", "")
            }
            
            # Using addition mode for atomicity
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=None, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving message: {e}")

        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        
        routes = {
            '/': 'index.html',
            '/message': 'message.html',
            '/message.html': 'message.html',
            '/read': self.handle_read_messages
        }

        if pr_url.path in routes:
            if callable(routes[pr_url.path]):
                routes[pr_url.path]()
            else:
                self.send_html_file(routes[pr_url.path])
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def handle_read_messages(self):
        template = self.get_template('read.html')
        
        try:
            with open('storage/data.json', 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = {}

        content = template.render(messages=messages)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())

    def send_html_file(self, filename, status=200):
        template = self.get_template(filename)
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = template.render()
        self.wfile.write(content.encode())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        print(f"Server started at http://localhost:3000")
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
