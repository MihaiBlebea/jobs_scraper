#!/bin/bash

echo "installing the database"
DB_FILE=./store.db
if test -f "$DB_FILE"; then
    echo "$DB_FILE exists. do not install db"
else
	echo "$DB_FILE does not exist. install db"
	sqlite3 store.db < ./init.sql
fi