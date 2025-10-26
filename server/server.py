import http.server
import socketserver
import os
import cgi


PORT = 8000


def add_log(sf):

  length = int(sf.headers['Content-Length'])
  form = cgi.FieldStorage(fp=sf.rfile, headers=sf.headers, environ={'REQUEST_METHOD': 'POST'}, keep_blank_values=True)

  fileitem = form['file']
  if not fileitem.file: return
  file_data = fileitem.file.read()

  with open('capturas.txt', 'wb') as f:
    f.write(file_data)

  sf.send_response(200)
  sf.send_header("Content-type", "text/html")
  sf.end_headers()
  sf.wfile.write(b"File uploaded successfully.")


def fail(sf):
  sf.send_response(404)
  sf.send_header("Content-type", "text/html")
  sf.end_headers()
  sf.wfile.write(b"404 Not Found")


class CustomHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/log":
          add_log(self)
        else:
          fail(self)


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"serving at port {PORT}")
    httpd.serve_forever()

