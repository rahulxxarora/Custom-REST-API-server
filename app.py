import BaseHTTPServer
import os
import json
import re
import base64


class TemporaryDatabase(object):
	items = {
		'foo':{'id':'foo', 'seller':'bar', 'price':'99'},
	}

	users = {
		'root':'cm9vdDpwd2Q='
	}

class SimpleRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def _set_headers(self, response_code=200):
		self.send_response(response_code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def auth(f):
		def wrapper(self):
			_args = re.findall(r'/\w+', self.path)

			print self.path

			if _args[0][1:] == 'user':
				return f(self)

			try:
				if self.headers['Authorization'] and self.headers['user']:
					if TemporaryDatabase.users.has_key(self.headers['user']) and self.headers['Authorization'] == 'Basic ' + TemporaryDatabase.users[self.headers['user']]:
						return f(self)
					else:
						self._set_headers(401)
						self.wfile.write(bytes(json.dumps({'msg':'Unauthorized request'})))
			except:
				self._set_headers(400)
				self.wfile.write(bytes(json.dumps({'msg':'Invalid request'})))
		
		return wrapper

	@auth
	def do_GET(self):
		_args = re.findall(r'/\w+', self.path)

		if len(_args) == 0 or len(_args) > 2 or _args[0] != '/products':
			data = json.dumps({'msg':'Invalid request'})
			self._set_headers(400)
		elif len(_args) == 1:
			# List all items
			data = json.dumps(TemporaryDatabase.items)
			self._set_headers(200)
		elif len(_args) == 2:
			# List a specific item
			try:
				data = json.dumps(TemporaryDatabase.items[_args[1][1:]])
				self._set_headers(200)
			except: # Key error
				data = json.dumps({'msg':'Item not found'})
				self._set_headers(404)

		self.wfile.write(bytes(data))

	@auth
	def do_POST(self):
		_args = re.findall(r'/\w+', self.path)
		content_length = int(self.headers['Content-Length'])
		req_data = json.loads(self.rfile.read(content_length))

		if _args[0] == '/user':
			user = req_data['user']
			pwd = req_data['pwd']
			key = user + ':' + pwd
			auth_token = base64.b64encode(key.encode('utf-8'))

			TemporaryDatabase.users[user] = auth_token

			data = json.dumps({'Auth Token':auth_token})
		else:
			TemporaryDatabase.items[req_data['id']] = req_data
			data = json.dumps({'msg':'Item stored in the database'})

		self._set_headers(201)
		self.wfile.write(bytes(data))

	@auth
	def do_PUT(self):
		content_length = int(self.headers['Content-Length'])
		req_data = json.loads(self.rfile.read(content_length))
		
		TemporaryDatabase.items[req_data['id']] = req_data	

		self._set_headers(200)
		self.wfile.write(bytes(json.dumps({'msg':'Item updated in the database'})))

	@auth
	def do_DELETE(self):
		_args = re.findall(r'/\w+', self.path)

		if len(_args) == 0 or len(_args) > 2 or _args[0] != '/delete':
			data = json.dumps({'msg':'Invalid endpoint'})
			self._set_headers(400)
		else:
			try:
				del  TemporaryDatabase.items[_args[1][1:]]
				self._set_headers(200)
				data = json.dumps({'msg':'Item deleted successfully'})
			except:
				self._set_headers(404)
				data = json.dumps({'msg':'Item not found'})

		self.wfile.write(bytes(data))

def run(server_class=BaseHTTPServer.HTTPServer, handler_class=SimpleRequestHandler):
	port = int(os.environ.get('PORT', 8000))
	print 'Starting server on port ' + str(port)
	server_address = ('0.0.0.0', port)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()

if __name__ == '__main__':
    run()