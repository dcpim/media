""" DCPIM is a general purpose Python 3.x library that contains a lot of
	commonly done operations inside of a single package. (C) 2018-2024
	Patrick Lambert - http://dendory.net - Provided under the MIT License
"""

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
		valid_until = dcpim.db_get(
			"dcpim.sessions.{}".format(token),
			"valid_until"
		)
		from_ip = dcpim.db_get(
			"dcpim.sessions.{}".format(token),
			"from_ip"
		)
	except:
		output['message'] = "Invalid login token."
		return output

	# Make sure session isn't expired
	if dcpim.days_since(valid_until) > 0:
		output['message'] = "Login token expired on {}." \
		.format(valid_until)
		return output

	# Make sure the session IP is valid
	if from_ip != request.remote_addr:
		output['message'] = "Login token is not valid from {}." \
		.format(request.remote_addr)
		return output

	output['status'] = 0
	return output


@app.route('/', methods=['GET', 'POST'])
def index():
	""" Default route is unused. """
	output = {
		'status': 1,
		'message': "No action specified.",
		'data': []
	}
	return jsonify(output)


@app.route('/library', methods=['GET', 'POST'])
def library():
	""" library - Lists the items in a user's music library.
 			@param token: Valid logged in token
 	"""
	output = validate()
	if output['status'] == 1:
		return jsonify(output)

	output['message'] = "Success."
	return jsonify(output)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
