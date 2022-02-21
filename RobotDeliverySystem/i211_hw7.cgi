#! /usr/bin/env python3
print('Content-type: text/html\n')

import cgi

form = cgi.FieldStorage()  

html = """<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Robot Delivery</title></head>
	</head>
	<body>
		<h1> Robot Delivery System Confirmation</h1>
		<p>You have selected to have a {0} delivered by {1}</p>
		<p>Your total comes to ${2}</p>
	</body>
</html>"""

item = form.getfirst('delivery','unknown item')
delivery = form.getfirst('delivery_method', 'drone')
cost = form.getfirst('cost', '0') 

total = 0

if delivery == "drone":
	total = int(cost) + 10
elif delivery == "self driving car":
	total = int(cost) + 20
elif delivery == "giant robot":
	total = int(cost) + 1000
else:
	total = int(cost) + 10

print(html.format(item, delivery, total))