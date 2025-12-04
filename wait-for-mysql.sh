#!/bin/bash
HOST=$1
shift
CMD="$@"

MYSQL_USER=${DB_USER:-root}
MYSQL_PASSWORD=${DB_PASSWORD:-Mpumi777}

echo "Waiting for MariaDB at $HOST..."

until mysql -h "$HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1" &> /dev/null
do
  echo "Waiting for MariaDB at $HOST..."
  sleep 2
done

echo "MariaDB is up - executing command"
exec $CMD
