#!/bin/bash

set -e
set -u

function create_user_and_database() {
	local database=$1
	echo "Creating database '$database'"
	# Check if database already exists
	if psql -U "$POSTGRES_USER" -lqt | cut -d \| -f 1 | grep -qw "$database"; then
		echo "Database '$database' already exists, skipping..."
	else
		psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
		    CREATE DATABASE "$database";
		    GRANT ALL PRIVILEGES ON DATABASE "$database" TO "$POSTGRES_USER";
EOSQL
	fi
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
	echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
	for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
		# Skip the default database (already created by POSTGRES_DB)
		if [ "$db" != "$POSTGRES_DB" ]; then
			create_user_and_database $db
		fi
	done
	echo "Multiple databases created"
fi

