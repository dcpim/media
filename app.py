""" DCPIM is a general purpose Python 3.x library that contains a lot of
	commonly done operations inside of a single package. (C) 2018-2024
	Patrick Lambert - http://dendory.net - Provided under the MIT License
"""

import os
import json
from flask import Flask, jsonify, request
import dcpim

app = Flask(__name__)

def validate():
	""" Check for a valid login token. """
	output = {
		'status': 1,
		'message': "",
		'data': []
	}

	# Make sure the token is in the form
	if "token" not in request.form:
		output['message'] = "No login token specified."
		return output

	# Sanitize token
	token = dcpim.alphanum(request.form['token'])

	# Make sure the session exists for that token
	try:
		session = json.loads(dcpim.db_get(
			"dcpim.sessions",
			token
		))
		valid_until = session['valid_until']
		from_ip = session['from_ip']
	except Exception as err:
		output['message'] = "Invalid login token: {}".format(err)
		return output, None

	# Make sure session isn't expired
	if dcpim.days_since(valid_until) > 0:
		output['message'] = "Login token expired on {}." \
		.format(valid_until)
		return output, None

	# Make sure the session IP is valid
	if from_ip != request.remote_addr:
		output['message'] = "Login token is not valid from {}." \
		.format(request.remote_addr)
		return output, None

	output['status'] = 0
	return output, session


@app.route('/', methods=['GET', 'POST'])
def index():
	""" Default route is unused. """
	output = {
		'status': 1,
		'message': "No action specified.",
		'data': []
	}
	return jsonify(output)


@app.route('/initialize', methods=['GET', 'POST'])
def initialize():
	""" initialize - Initialize basic settings for a user.
 			@param token: Valid logged in token
 	"""
	(output, session) = validate()
	if output['status'] == 1:
		return jsonify(output)

	token = dcpim.alphanum(request.form['token'])
	env = 

	try:
		dcpim.db_create("dcpim.{}.media.music.{}".format(
			os.environ['DCPIM_ENV'],
			session['username']
		))
		output['data'].append("Music library created.")
	except:
		output['data'].append("Music library already existed.")

	try:
		dcpim.db_create("dcpim.{}.media.videos.{}".format(
			os.environ['DCPIM_ENV'],
			session['username']
		))
		output['data'].append("Video library created.")
	except:
		output['data'].append("Video library already existed.")

	output['message'] = "Success."
	
	return jsonify(output)


@app.route('/music', methods=['GET', 'POST'])
def music():
	""" music - Lists the items in a user's music library.
 			@param token: Valid logged in token
 	"""
	(output, session) = validate()
	if output['status'] == 1:
		return jsonify(output)

	try:
		output['data'] = dcpim.db_get("dcpim.{}.media.music.{}".format(
			os.environ['DCPIM_ENV'],
			session['username']
		))
		output['message'] = "Success."
	except:
		output['status'] = 1
		output['message'] = "User library has not been initialized."
	
	return jsonify(output)


@app.route('/videos', methods=['GET', 'POST'])
def videos():
	""" videos - Lists the items in a user's video library.
 			@param token: Valid logged in token
 	"""
	(output, session) = validate()
	if output['status'] == 1:
		return jsonify(output)

	try:
		output['data'] = dcpim.db_get("dcpim.{}.media.videos.{}".format(
			os.environ['DCPIM_ENV'],
			session['username']
		))
		output['message'] = "Success."
	except:
		output['status'] = 1
		output['message'] = "User library has not been initialized."
	
	return jsonify(output)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
