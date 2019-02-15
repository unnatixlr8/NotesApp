# NotesApp
Infosys Project

install python 3.

install venv and activate it.

`pip install mysql-connector-python`

Make a database with a name **python** and password *pythondb*

Then make a table **notes**

```
CREATE TABLE notes (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
note TEXT);
```



