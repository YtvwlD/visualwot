def get_html(html_file):
	with open("inc/html/{}.htm".format(html_file)) as handle:
		content = handle.read()
	return(content)
