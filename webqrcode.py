#!/usr/bin/env python
import os.path

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.autoreload
import tornado.options
from tornado.options import define, options

import qrcode
from cStringIO import StringIO

define('port', default=8000, help='run on the listen port', type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')


class QrStreamHandler(tornado.web.RequestHandler):
	def get(self):
		qrsize = int(self.get_argument('size', '10'))
		qrborder = int(self.get_argument('border', '1'))
		dl = self.get_argument('dl', 'off')
		url = self.get_argument('url', '')
		self.set_header("Content-Type", "image/png")
		if dl == 'on':
			self.set_header("Content-Disposition", "attachment")
		if qrsize > 100:
			qrsize = 100
		if qrborder > 100:
			qrborder = 100
		qr = qrcode.QRCode(
			 version=2
			,error_correction=qrcode.constants.ERROR_CORRECT_H
			,box_size=qrsize
			,border=qrborder
		)
		qr.add_data(url)
		img = qr.make_image()
		new_img = StringIO()
		img.save(new_img, "PNG")
		self.write(new_img.getvalue())

app = tornado.web.Application(
    handlers=[
        (r"/", IndexHandler)
        ,(r"/qrcode/", QrStreamHandler)
    ]
    ,template_path=os.path.join(os.path.dirname(__file__), 'tmpl')
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    loop=tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
