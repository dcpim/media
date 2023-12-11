"""Run tests for DCPIM media."""

import json
import dcpim


# Mock session
token = dcpim.guid()
table = "dcpim.sessions.{}".format(token)
dcpim.db_create(table)
dcpim.db_put(table, "valid_until", "2038-01-01 12:00:00")
dcpim.db_put(table, "from_ip", "172.17.0.1")
dcpim.db_put(table, "username", "admin")
dcpim.db_put(table, "roles", "|media.admin|")
print("Session table created:")
print(dcpim.db_get(table))


# Run tests
status = 0
result = json.loads(dcpim.curl("http://127.0.0.1/library", data={'token': token}))
print(result)
if result['status'] != 0:
	status = result['status']


# Evaluate status and delete session
dcpim.db_delete(table)
print("Tests done.")
exit(status)
