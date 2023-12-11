"""Run tests for DCPIM media."""

import dcpim
import boto3

# Mock session
mock_token = dcpim.guid()
mock_table = "dcpim.sessions.{}".format(token)
dcpim.db_create(mock_table)
dcpim.db_put(mock_table, "valid_until", "2038-01-01 12:00:00")
dcpim.db_put(mock_table, "from_ip", "127.0.0.1")
dcpim.db_put(mock_table, "username", "admin")
dcpim.db_put(mock_table, "roles", "|media.admin|")


# Run tests


# Delete session
dcpim.db_delete(mock_table)
