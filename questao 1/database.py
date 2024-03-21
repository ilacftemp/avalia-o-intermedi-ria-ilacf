import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int=None
    title: str=None
    content: str=''

class Database():
    def __init__(self, banco):
        self.banco = banco
        self.conn = sqlite3.connect(banco+".db")
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL);")

    def add(self, note):
        comando = f'INSERT INTO note (title, content) VALUES (\'{note.title}\', \'{note.content}\');'
        self.conn.execute(comando)
        self.conn.commit()

    def get_all(self):
        comando = f"SELECT id, title, content FROM note"
        cursor = self.conn.execute(comando)
        notes = []
        for linha in cursor:
            id = linha[0]
            titulo = linha[1]
            conteudo = linha[2]
            note = Note(id, titulo, conteudo)
            notes.append(note)
        return notes
    
    def update(self, entry):
        comando = f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}"
        self.conn.execute(comando)
        self.conn.commit()

    def delete(self, note_id):
        comando = f"DELETE FROM note WHERE id = {note_id}"
        self.conn.execute(comando)
        self.conn.commit()

    def get_one(self, id):
        cursor = self.conn.execute(f"SELECT id, title, content FROM note WHERE id = {id}")
        nota = [Note(linha[0], linha[1], linha[2]) for linha in cursor]
        return nota[0]