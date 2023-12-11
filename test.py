"""Run tests for DCPIM media."""

import json
import dcpim


# Mock session
TOKEN = dcpim.guid()
TABLE = "dcpim.sessions.{}".format(TOKEN)
dcpim.db_create(TABLE)
dcpim.db_put(TABLE, "valid_until", "2038-01-01 12:00:00")
dcpim.db_put(TABLE, "from_ip", "172.17.0.1")
dcpim.db_put(TABLE, "username", "admin")
dcpim.db_put(TABLE, "roles", "|media.admin|")
print("Session table created:")
print(dcpim.db_get(TABLE))


# Run tests
status = 0
result = json.loads(dcpim.curl("http://127.0.0.1/library", data={'token': TOKEN}))
print(result)
if result['status'] != 0:
	status = result['status']


# Evaluate status and delete session
dcpim.db_delete(TABLE)
print("Tests done.")
if status != 0:
	quit(1)
