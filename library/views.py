from pathlib import Path
from django.conf import settings
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import DownloadLog, Favorite


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


@login_required
def download_music(request, filename):
    root = settings.MUSIC_ROOT.resolve()
    try:
        file_path = (root / filename).resolve(strict=True)
        file_path.relative_to(root)  # prevents path traversal
    except (FileNotFoundError, ValueError):
        raise Http404("File not found.")

    # FLAW 1: Broken Access Control (A01:2021)
    # Any authenticated user can download any file. The application does not verify
    # whether the file is authorized for that user

    # Suggested fix :
    # if not DownloadPermission.objects.filter(user=request.user, filename=filename).exists():
    #     raise Http404("You don't have access to this file.")

    # log the download
    DownloadLog.objects.create(user=request.user, filename=filename)

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)


@login_required
def toggle_favorite(request, filename):
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

# FLAW 4: SQL Injection (A03:2021)
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

# suggested fix :
# use Django's ORM or parameterized SQL instead:
#
# results = User.objects.filter(username__icontains=query).values_list('id', 'username')
