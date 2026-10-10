import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Author, Book


@require_GET
def author_list(request):
    authors = Author.objects.all()

    name = request.GET.get('name')
    if name:
        authors = authors.filter(name__icontains=name)

    data = [
        {
            'id': author.id,
            'name': author.name,
            'email': author.email,
        }
        for author in authors
    ]

    return JsonResponse(data, safe=False)


@require_GET
def book_list(request):
    books = Book.objects.select_related('author').all()

    available = request.GET.get('available')
    if available is not None:
        if available.lower() == 'true':
            books = books.filter(is_available=True)
        elif available.lower() == 'false':
            books = books.filter(is_available=False)
        else:
            return JsonResponse(
                {'error': 'available must be true or false'},
                status=400
            )

    author_id = request.GET.get('author_id')
    if author_id is not None:
        try:
            author_id = int(author_id)
        except (ValueError, TypeError):
            return JsonResponse(
                {'error': 'author_id must be an integer'},
                status=400
            )

        books = books.filter(author__id=author_id)

    title = request.GET.get('title')
    if title:
        books = books.filter(title__icontains=title)

    data = [
        {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'is_available': book.is_available,
            'author': {
                'id': book.author.id,
                'name': book.author.name,
            },
        }
        for book in books
    ]

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def create_author(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {'error': 'JSON body must be an object'},
            status=400
        )

    name = data.get('name')
    email = data.get('email')

    if not isinstance(name, str) or not name.strip():
        return JsonResponse(
            {'error': 'Valid name is required'},
            status=400
        )

    if not isinstance(email, str) or not email.strip():
        return JsonResponse(
            {'error': 'Valid email is required'},
            status=400
        )

    name = name.strip()
    email = email.strip()

    if Author.objects.filter(email=email).exists():
        return JsonResponse(
            {'error': 'This email already exists'},
            status=400
        )

    author = Author.objects.create(
        name=name,
        email=email
    )

    return JsonResponse(
        {
            'id': author.id,
            'name': author.name,
            'email': author.email,
        },
        status=201
    )


@csrf_exempt
@require_POST
def create_book(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {'error': 'JSON body must be an object'},
            status=400
        )

    title = data.get('title')
    description = data.get('description', '')
    author_id = data.get('author_id')

    if not isinstance(title, str) or not title.strip():
        return JsonResponse(
            {'error': 'Valid title is required'},
            status=400
        )

    if not isinstance(description, str):
        return JsonResponse(
            {'error': 'Description must be a string'},
            status=400
        )

    if isinstance(author_id, bool) or author_id is None:
        return JsonResponse(
            {'error': 'author_id is required and must be an integer'},
            status=400
        )

    try:
        author_id = int(author_id)
    except (ValueError, TypeError):
        return JsonResponse(
            {'error': 'author_id must be an integer'},
            status=400
        )

    if author_id <= 0:
        return JsonResponse(
            {'error': 'author_id must be positive'},
            status=400
        )

    author = Author.objects.filter(id=author_id).first()

    if author is None:
        return JsonResponse(
            {'error': 'Author not found'},
            status=404
        )

    book = Book.objects.create(
        title=title.strip(),
        description=description,
        author=author
    )

    return JsonResponse(
        {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'is_available': book.is_available,
            'author_id': book.author_id,
        },
        status=201
    )