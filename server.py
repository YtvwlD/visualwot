#!/usr/bin/env python3
from os import path
from werkzeug.serving import run_simple
from werkzeug.wsgi import SharedDataMiddleware, DispatcherMiddleware
from werkzeug.wrappers import Request, Response

import index

@Request.application
def notfound(request):
	return Response("Not found.", 404)

app = SharedDataMiddleware(DispatcherMiddleware(notfound,
	{
	"/":			index.run,
	"/index.py":	index.run
	}),
	{
	"/css":		path.join(path.dirname(__file__), "css"),
	"/js":		path.join(path.dirname(__file__), "js"),
	"/img":		path.join(path.dirname(__file__), "img"),
	"/html":	path.join(path.dirname(__file__), "html"),
	"/fonts":	path.join(path.dirname(__file__), "fonts")
	})

if __name__ == "__main__":
	run_simple('127.0.0.1', 4000, app)
