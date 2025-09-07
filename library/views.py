from django.conf import settings
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import DownloadLog, Favorite, FilePermission


def _list_music_files():
    root = settings.MUSIC_ROOT
    root.mkdir(exist_ok=True)

    allowed = getattr(
        settings,
        'ALLOWED_EXTENSIONS',
        {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
    )

    files = [
        p.name for p in root.iterdir()
        if p.is_file() and p.suffix.lower() in allowed
    ]
    return sorted(files, key=str.lower)


@login_required
def music_list(request):
    files = _list_music_files()
    favorites = set(
        Favorite.objects.filter(user=request.user).values_list('filename', flat=True)
    )
    return render(request, 'library/list.html', {
        'files': files,
        'favorites': favorites
    })


# flaw 1: broken access control (a01:2021)  
# no permission checks; any user can download any file
@login_required
def download_music(request, filename):
    root = settings.MUSIC_ROOT.resolve()
    try:
        file_path = (root / filename).resolve(strict=True)
        file_path.relative_to(root)
    except (FileNotFoundError, ValueError):
        raise Http404("File not found.")

    # flaw 1: missing access control check
    # any user can download any file - no permission validation
    
    # fix: add permission check
    # if not FilePermission.objects.filter(user=request.user, filename=filename).exists():
    #     raise Http404("access denied")

    DownloadLog.objects.create(user=request.user, filename=filename)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)


@login_required
def toggle_favorite(request, filename):
    if request.method == 'POST':
        fav, created = Favorite.objects.get_or_create(user=request.user, filename=filename)
        if not created:
            fav.delete()
    return redirect('music_list')


@login_required
def user_activity(request):
    downloads = DownloadLog.objects.filter(user=request.user).order_by('-downloaded_at')
    favorites = Favorite.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'library/user_activity.html', {
        'downloads': downloads,
        'favorites': favorites
    })

from django.db import connection
from django.contrib.auth.models import User

# flaw 3: SQL Injection (A03:2021)
# This view runs a raw SQL query with user input directly inserted
# This can lead to SQL injection attacks if an attacker crafts a malicious query string

@login_required
def search_users(request):
    results = []
    query = request.GET.get('q')

    if query:
        with connection.cursor() as cursor:
            # Vulnerable query: user input is not sanitized
            cursor.execute(f"SELECT id, username FROM auth_user WHERE username LIKE '%{query}%'")
            results = cursor.fetchall()

    return render(request, 'library/search_users.html', {
        'results': results,
        'query': query
    })

# flaw 3 fix :
# use Django's ORM or parameterized SQL instead:
# results = User.objects.filter(username__icontains=query).values_list('id', 'username')
# 

# csrf exempt views for login/logout to work while flaw 2 is active
# fix: remove @csrf_exempt decorator when csrf middleware is enabled
@csrf_exempt
def custom_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('music_list')
            else:
                error = 'invalid credentials'
        else:
            error = 'username and password required'
    return render(request, 'registration/login.html', {'error': error})

# fix: remove @csrf_exempt decorator when csrf middleware is enabled
@csrf_exempt  
def custom_logout(request):
    logout(request)
    return redirect('login')
