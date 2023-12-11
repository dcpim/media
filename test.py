"""Run tests for DCPIM media."""

import dcpim
import boto3

# Mock session
TOKEN = dcpim.guid()
TABLE = "dcpim.sessions.{}".format(TOKEN)
dcpim.db_create(TABLE)
dcpim.db_put(TABLE, "valid_until", "2038-01-01 12:00:00")
dcpim.db_put(TABLE, "from_ip", "127.0.0.1")
dcpim.db_put(TABLE, "username", "admin")
dcpim.db_put(TABLE, "roles", "|media.admin|")


# Run tests


# Delete session
dcpim.db_delete(TABLE)
