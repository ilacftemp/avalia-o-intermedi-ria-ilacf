from utils import load_data, load_template, add_note, build_response
from urllib.parse import unquote_plus
from database import Database, Note

db = Database('notas')

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        titulo, detalhe = corpo.split("&")
        params['titulo'] = unquote_plus(titulo.split("=")[1], encoding='utf-8', errors='replace')
        params['detalhes'] = unquote_plus(detalhe.split("=")[1], encoding='utf-8', errors='replace')
        add_note(params)
        # ou, se eu quisesse fazer com for:
        # for chave_valor in corpo.split("&"):
        #     params[unquote_plus(chave_valor.split("=")[0], encoding='utf-8', errors='replace')] = unquote_plus(chave_valor.split("=")[1], encoding="utf-8", errors="replace")

        return build_response(code=303, reason='See Other', headers='Location: /')

    note_template = load_template("components/note.html")
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response(body=load_template('index.html').format(notes=notes))

def delete_note(id):
    db.delete(id)
    return build_response(code=303, reason='See Other', headers='Location: /')

def edit_note(request, id):
    nota = db.get_one(id)
    if request.startswith("POST"):
        request = request.replace('\r', '')
        partes = request.split('\n\n') 
        titulo, detalhe = partes[1].split("&")
        titulo = unquote_plus(titulo.split("=")[1], encoding='utf-8', errors='replace')
        detalhe = unquote_plus(detalhe.split("=")[1], encoding='utf-8', errors='replace')
        nota = Note(id, titulo, detalhe)
        db.update(nota)
        return build_response(code=303, reason='See Other', headers='Location: /')
    return build_response(body=load_template('edit.html').format(nota=nota))