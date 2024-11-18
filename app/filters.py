from aiohttp import web
from .models import Note


def get_note_filter(request: web.Request):
    return {
        "search": request.query.get("search", ""),
        "author": request.query.get("author", ""),
        "date_from": request.query.get("date_from", ""),
        "date_to": request.query.get("date_to", ""),
    }


def filter_notes(query, filters):
    if filters["search"]:
        # DJANGO query = query.filter(title__icontains=filters["search"])
        query = query.where(Note.title.ilike(f"%{filters['search']}%") | Note.content.ilike(f"%{filters['search']}%"))
    if filters["author"]:
        query = query.where(Note.author_id == filters["author"])
    if filters["date_from"]:
        query = query.where(Note.created_at >= filters["date_from"])
    if filters["date_to"]:
        query = query.where(Note.created_at <= filters["date_to"])
    return query
