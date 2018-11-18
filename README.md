# Gnomus server

This is a Flask app that is brains of the garden server, managing sensors defined in the [gnomus-sensors](https://github.com/matthoffman/gnomus-sensors) project.

It started from [JackStouffer's Flask-Foundation](https://github.com/JackStouffer/Flask-Foundation), so documentation at [https://jackstouffer.com/flask-foundation](https://jackstouffer.com/flask-foundation/) is relevant

This is very much a work in progress.  You'll notice, at this point in early development, that there's some excessively detailed design notes strewn about in files like this one.
That's because I find time to work on this in small increments, so it helps me to be overly explicit with what I'm thinking so that I can pick it up again later.

## Gnomus?

A word invented by Paracelsus in the 18th century to describe small earth-dwelling creatures; it became the English "gnome". 
The plan is for this server to manage sensors that are deployed in various places in the garden inside plastic garden gnomes, so the name seems appropriate.


# Design

## Database or Flat File Configuration?

My configuration data model is a set of garden beds (maybe 6 or 7?), a set of sensors (roughly 3-4 per bed, so < 20?), and maybe some global config. So that could be stored in a big JSON file, or set of JSON files, or it could be defined in an actual database.

I'd like it to be easy to backup and restore, and easy to modify as the garden setup changes. In most cases, I'd lean toward configuring it in text files (YAML or similar) on disk, and version the config in Git, so I could easily version it, roll back, etc. 
But in this particular case, I hope to manage it via a web UI, so for expedience's sake I plan on storing it in whatever form is easiest to manage via Flask, which might well be a simple database.

Now, the actual sensor readings are a bit different. They are much higher volume, and I want that to be backed up. They could be a set of log files, or could be a proper database. Not sure what a proper database buys me, but then again, I'm not sure what it really costs me either. That is really the problem SQLite is trying to solve (from their webpage): 
> SQLite does not compete with client/server databases. SQLite competes with fopen().

So, that's probably the expedient option. We're not looking at more volume that SQLite can handle, certainly.


## Visualization

 - Get all locations. 
 - For each, get all sensors for that location.
 - For each sensor, look up all sensor readings. Plot them on a graph. Label the graph with the sensor's name.

There's still a fair chance that I'll integrate an existing graphing / visualization solution here instead of rolling my own. 
I'm intentionally rolling my own sensor code, because it's an excuse to work with Micropython and it's fun, but I 
don't feel any need to reinvent the millions of graphing and charting solutions that already exist. We'll see what ends 
up being most expedient.


# TODO



## Backing up the database

To make a backup copy of the database, you can use the built-in "backup" command:

```
sqlite3 database.db  ".backup database.db.bak"
```

Or simply do a "dump" and redirect the results to a file. Not sure why you'd do this, though, honestly:

```
sqlite3 database.db .dump > database.db.bak
```

## Restoring the database

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


Of course, you can also back up and restore using the web services to output JSON. 


