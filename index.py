#!/usr/bin/env python3
from werkzeug.wrappers import Request, Response

from get_html import get_html

@Request.application
def run(request):
	html = get_html("index")
	return Response(html, mimetype="text/html")

if __name__ == "__main__":
	import CGI
	CGI.app = run
	CGI.run()
