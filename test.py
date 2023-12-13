"""Run tests for DCPIM media."""

import json
import dcpim


# Mock session
token = dcpim.guid(32)
data = {
	'valid_until': "2038-01-01 12:00:00",
	'from_ip': "172.17.0.1",
	'username': "admin",
	'roles': "|media.admin|"
}
table = "dcpim.test.sessions"
try:
	dcpim.db_create(table)
	print("Session table created.")
except:
	pass
dcpim.db_put(table, token, str(data))
print("Admin token created:")
print(dcpim.db_get(table, token))


# Run tests
result = json.loads(dcpim.curl("http://127.0.0.1/initialize", data={'token': token}))
print(result)
assert result['status'] == 0
result = json.loads(dcpim.curl("http://127.0.0.1/music", data={'token': token}))
print(result)
assert result['status'] == 0
result = json.loads(dcpim.curl("http://127.0.0.1/videos", data={'token': token}))
print(result)
assert result['status'] == 0

# Tests done.
print("Tests done.")
quit()
