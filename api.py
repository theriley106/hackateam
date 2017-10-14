from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import login


app = Flask(__name__)



@app.route('/login&<username>&<password>')
def fileDownloading(username, password):
	print username
	print password
	return str(login.login(username, password))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)