"""Run tests for DCPIM media."""

import dcpim
import boto3

# Mock session
token = dcpim.guid()
table = "dcpim.sessions.{}".format(token)
dcpim.db_create(table)
dcpim.db_put(table, "valid_until", "2038-01-01 12:00:00")
dcpim.db_put(table, "from_ip", "127.0.0.1")
dcpim.db_put(table, "username", "admin")
dcpim.db_put(table, "roles", "|media.admin|")


# Run tests


# Delete session
dcpim.db_delete(table)
