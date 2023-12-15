""" DCPIM is a general purpose Python 3.x library that contains a lot of
	commonly done operations inside of a single package.
	(C) 2018-2024 Patrick Lambert - Provided under the MIT License
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
			"dcpim.{}.sessions".format(
				os.environ['DCPIM_ENV']
			),
			token
		).replace("'",'"'))
		valid_until = session['valid_until']
		from_ip = session['from_ip']
	except:
		output['message'] = "Invalid login token."
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	""" Default route is unused. """
	output = {
		'status': 1,
		'message': "Invalid action specified.",
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


@app.route('/music/list', methods=['GET', 'POST'])
def music_list():
	""" music/list - Lists the items in a user's music library.
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


@app.route('/music/add', methods=['GET', 'POST'])
def music_add():
	""" music/add - Add a music to the library.
 			@param token: Valid logged in token
    			@source string: The source type
       			@url string: The source URL
	  		@name string: The name of the song
 	"""
	(output, session) = validate()
	if output['status'] == 1:
		return jsonify(output)

	# Make sure all parameters are in the request
	if 'source' not in request.form or 'url' not in request.form or \
	'name' not in request.form:
		output['status'] = 1
		output['message'] = "Form must include: source, url, name."
		return jsonify(output)

	# Setup variables for bucket, name of music and filename
	bucket = "s3://dcpim-media-{}/".format(
		os.environ['DCPIM_ENV']
	)
	name = dcpim.alphanum(
		request.form['name'],
		symbols=True,
		spaces=True
	)
	filename = "{}.mp3".format(dcpim.guid())
	prefix = "{}/{}".format(
		session['username'],
		filename
	)

	# Download music from URL
	if str(request.form['source']).lower() == "url":
		try:
			size = dcpim.download(request.form['url'], filename)
		except Exception as err:
			output['status'] = 1
			output['message'] = "Download failed: {}".format(err)
			return jsonify(output)

	# Download music from YouTube
	elif str(request.form['source']).lower() == "youtube":
		output['status'] = 1
		output['message'] = "Not implemented."
		return jsonify(output)

	# Invalid source type
	else:
		output['status'] = 1
		output['message'] = "Source type must be one of: url, youtube"
		return jsonify(output)

	# Upload music to S3
	s3 = boto3.client('s3')
	try:
		response = s3.upload_file(
			filename,
			bucket,
			prefix
		)
	except Exception as err:
		output['status'] = 1
		output['message'] = "Upload failed: {}".format(err)
		return jsonify(output)

	# Set data to add to library and add to DB
	data = {
		'filename': prefix,
		'size': size
	}
	dcpim.db_put(
		"dcpim.{}.media.videos.{}".format(
			os.environ['DCPIM_ENV'],
			session['username']
		),
		name,
		data
	)
	output['data'].append(data)
	output['message'] = "Success"

	return jsonify(output)


@app.route('/videos/list', methods=['GET', 'POST'])
def videos_list():
	""" videos/list - Lists the items in a user's video library.
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
