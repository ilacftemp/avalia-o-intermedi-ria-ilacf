from django.shortcuts import render, redirect
from .models import Note, Tag, Fact
# from urls import urlpatterns

# username: ila
# email: ilachafin
# password: nesquece

def index(request):  
    all_tags = Tag.objects.all() 
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = request.POST.get('tag')
        if tag == '':
            Note.objects.create(title=title, content=content)
        else:
            Note.objects.create(title=title, content=content, tag=tag)
            all_tags = Tag.objects.all()
            test_tag = Tag(title=tag)
            title_list = []
            for tagg in all_tags:
                title_list.append(tagg.title)
            if test_tag.title not in title_list:
                Tag.objects.create(title=tag)
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})    
    
def delete(request, id):
    nota = Note.objects.get(id=id)
    if nota.tag != '':
        tag = Tag.objects.get(title=nota.tag)
        notas = Note.objects.filter(tag=tag.title)
        qntd_notas = len(notas)
        if qntd_notas == 0:
            tag.delete()
    nota.delete()
    return redirect('index')

def edit(request, id):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        Note.objects.filter(id=id).update(title=title, content=content)
        return redirect('index')
    else:
        nota = Note.objects.filter(id=id).values()[0]
        return render(request, 'notes/edit.html', {'title': nota['title'], 'content': nota['content']})
    
def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})    

def tag(request, title):
    tag = Tag.objects.get(title=title)
    notas = Note.objects.filter(tag=tag.title)
    return render(request, 'notes/tag_especifica.html', {'tag':tag, 'notas': notas})

def delete_pag_tag(request, id):
    nota = Note.objects.get(id=id)
    nome_tag = nota.tag
    tag = Tag.objects.get(title=nome_tag)
    nota.delete()
    notas = Note.objects.filter(tag=tag.title)
    qntd_notas = len(notas)
    if qntd_notas == 0:
        tag.delete()
    return redirect('index')
    # else:
    #     return render(request, 'notes/tag_especifica.html', {'tag': tag, 'notas': notas})
    
def edit_pag_tag(request, id):
    nota = Note.objects.get(id=id)
    tag = Tag.objects.get(title=nota.tag)
    notas = Note.objects.filter(tag=nota.tag)
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        Note.objects.filter(id=id).update(title=title, content=content)
        # return render(request, 'notes/tag_especifica.html', {'tag':tag, 'notas': notas})
        return redirect('index')
    else:
        nota = Note.objects.filter(id=id).values()[0]
        return render(request, 'notes/edit.html', {'title': nota['title'], 'content': nota['content']})

def delete_tag(request, title):
    tag = Tag.objects.get(title=title)
    notas = Note.objects.filter(tag=tag.title)
    for nota in notas:
        nota.delete()
    tag.delete()
    tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': tags})

def facts(request):
    facts = Fact.objects.all()
    if request.method == 'POST':
        description = request.POST.get('description')
        Fact.objects.create(description=description)
    return render(request, 'notes/fact.html', {'facts': facts, 'qntd': len(facts)})
    
def like(request, description):
    fact = Fact.objects.get(description=description)
    likes = fact.likes + 1
    Fact.objects.filter(description=description).update(likes = likes)
    return redirect('index')