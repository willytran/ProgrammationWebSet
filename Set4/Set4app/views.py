from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import entries 

def index(request):
    if entries:
        entries_list = entries[::-1]  # reverse the order of entries
        highlight_id = entries_list[0]['id']  # set highlight ID to the last entry
    else:
        entries_list = []
        highlight_id = None
    return render(request, 'index.html', {'entries': entries_list, 'highlight_id': highlight_id})



def add(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        name = request.POST.get('name')
        if content and name:
            content = content.strip()
            name = name.strip().capitalize()
            if len(content) >= 10 and len(content) <= 120 and len(name) <= 20:
                entry_id = len(entries) + 1
                entry = {'id': entry_id, 'content': content, 'name': name}
                entries.insert(0, entry)
                return redirect('index')
            else:
                errors = ['Invalid input. Content must be between 10 and 120 characters long, and name must not exceed 20 characters.']
                return render(request, 'add.html', {'errors': errors, 'name': name, 'content': content})
        else:
            errors = ['Invalid input. Please enter both content and name.']
            return render(request, 'add.html', {'errors': errors, 'name': name, 'content': content})
    return render(request, 'add.html')



def entry(request, id):
    try:
        entry = entries[int(id)-1]
    except (IndexError, ValueError):
        entry = None
    if entry:
        return JsonResponse(entry)
    else:
        return JsonResponse({'error': 'Entry not found'})
