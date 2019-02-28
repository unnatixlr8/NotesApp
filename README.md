# NotesApp
Infosys Project

install python 3.

install venv and activate it.

`pip install mysql-connector-python`

Make a database with a name **python** and password *pythondb*

Then make a table **notes**

```sql
CREATE TABLE notes (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,,
 `uname` varchar(15) NOT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
note TEXT,FOREIGN KEY (`uname`) REFERENCES `users` (`uname`));
```
Make table **users**

```sql
CREATE TABLE `python`.`users` ( `uname` VARCHAR(15) NOT NULL , `upass` VARCHAR(15) NOT NULL , PRIMARY KEY (`uname`));
```
