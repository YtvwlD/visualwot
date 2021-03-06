from wsgiref.handlers import CGIHandler
from werkzeug.wrappers import Request, Response
#from werkzeug.debug import DebuggedApplication

from get_html import get_html

app = None

try:
	from sentry import Client
	client = Client()
except ImportError: #if Sentry isn't configured, everything is alright, but if Sentry failed to initialize, this should clearly raise an exception
	client = None

def run():
	CGIHandler().run(runSentry)
	#CGIHandler().run(DebuggedApplication(app))


def runSentry(environ, start_response):
	try:
		return (app(environ, start_response))
	except: #This is really neeed. If _anything_ goes wrong, display an error page.
		html = get_html("500")
		try:
			client.captureException()
			#html = html.replace("<!-- log >", "").replace("< /log -->", "")
		except: #Well, and even if we can't log the exception, we still need an error page.
			pass
			#html = html.replace("<!-- nolog >", "").replace("< /nolog -->", "")
		response = Response(html, 500, mimetype="text/html")
		return response(environ, start_response)
