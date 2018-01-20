# Garden Server

This is a Flask app that will hopefully be the brains of the garden server.
We'll see...

It started from https://github.com/JackStouffer/Flask-Foundation, so documentation at https://jackstouffer.com/flask-foundation/ is relevant


Some design notes and thoughts: 
1. I'm wondering if a database might be too much for this. My configuration data model is a set of garden beds (maybe 6 or 7?), a set of sensors (roughly 3-4 per bed, so < 20?), and maybe some global config. So that could be stored in a big JSON file, or set of JSON files. 

Now, the actual sensor readings need to be in some kind of datastore, and I want that to be backed up. Could be a set of log files, or could be a proper database. Not sure what a proper database buys me, but then again, I'm not sure what it really costs me either. That is really the problem SQLite is trying to solve: 
> SQLite does not compete with client/server databases. SQLite competes with fopen().



# Backing up the database

To make a backup copy of the database, you can use the built-in "backup" command:

```
sqlite3 database.db  ".backup database.db.bak"
```

Or simply do a "dump" and redirect the results to a file. Not sure why you'd do this, though, honestly:

```
sqlite3 database.db .dump > database.db.bak
```

# Restoring the database

To restore a database taken from "backup", you use "restore": 
```
sqlite3 database.db  ".restore database.db.bak"
```

If you used the "dump" method instead, you'd use this option instead: 

```
mv database.db database.db.old
sqlite3 database.db < database.db.bak
```

After restoring, verify the results.

```
sqlite3 database.db 'select * from users;'
```
(or pick the table of choice, obviously)
