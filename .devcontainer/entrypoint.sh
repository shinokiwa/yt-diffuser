#!/bin/bash
exec > >(tee /var/log/entrypoint.log) 2>&1
echo "entrypoint.sh is running"

. /server_start.sh

/usr/bin/tail -f /dev/null
