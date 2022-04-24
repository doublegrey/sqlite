import os
from datetime import datetime
import sqlite3
import uuid

# remove notes.db file. We do it only for testing purposes. Remove this line if you don't want to lose your data :)
try:
    os.remove("notes.db")
except:
    pass


# open local file as sql database. It will automatically create file, if it doesn't exist
db = sqlite3.connect('notes.db')


def init_table():
    # create table in database. We should execute this only once. If 'notes' table already exists, function will throw error
    db.execute(
        "CREATE TABLE notes (id TEXT, created TEXT, title TEXT, description TEXT, status BOOL)")


def find_all():
    notes = []
    # select all notes from db
    for row in db.execute("SELECT * FROM notes"):
        # db.execute returns list of tuples. We convert tuple to Note class
        note = Note(id=row[0], created=datetime.strptime(row[1], "%d.%m.%Y %H:%M:%S"), title=row[2],
                    description=row[3], status=row[4])
        notes.append(note)
    return notes


def print_notes(notes):
    for note in notes:
        print("* "+note.title)


class Note:
    def __init__(self, id=None, created=datetime.now(), title="", description="", status=True):
        if not id:
            id = uuid.uuid4().hex
        self.id = id
        self.created = created
        self.title = title
        self.description = description
        self.status = status

    def create(self):
        db.execute("""INSERT INTO notes (id, created, title, description, status) VALUES (?, ?, ?, ?, ?)""", (self.id, self.created.strftime(
            "%d.%m.%Y %H:%M:%S"), self.title, self.description, self.status))
        db.commit()

    def update(self):
        db.execute("""UPDATE notes SET created = ?, title = ?, description = ?, status = ? WHERE id = ?""", (self.created.strftime(
            "%d.%m.%Y %H:%M:%S"), self.title, self.description, self.status, self.id))
        db.commit()

    def delete(self):
        db.execute("DELETE FROM notes WHERE id=?", (self.id,))
        db.commit()


init_table()


note_1 = Note(created=datetime.now(), title="note 1",
              description="first note", status=True)
note_1.create()

note_2 = Note(created=datetime.now(), title="note 2",
              description="seVond note", status=True)
note_2.create()
note_2.description = "second note"
note_2.update()

notes = find_all()
print_notes(notes)
print("=============")
note_1.delete()
notes = find_all()
print_notes(notes)
