import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book
from libraryapp.models import model_factory
from ..connection import Connection

# this function handles HTTP requests given book info from models
# book can now only be viewed if user is authenticated using Django provided decorator
@login_required
def book_list(request):
    if request.method == 'GET':
        # connection is passed in with the db absolute path
        with sqlite3.connect(Connection.db_path) as conn:
            # Replaces conn.row_factory = sqlite3.Row, can only specify one row factory
            conn.row_factory = model_factory(Book)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                b.id,
                b.title,
                b.isbn,
                b.author,
                b.year_published,
                b.publisher,
                b.librarian_id,
                b.location_id
            from libraryapp_book b
            """)
            # fetchall gets list of tuples, row factory executes to turn into book objects
            all_books = db_cursor.fetchall()
        # template is holding the template created in templates folder
        template = 'books/list.html'
        context = {
            'all_books': all_books
        }
        # takes in the HTTP request, specified template, and dictionary of data to be used
        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_book
            (
                title, author, isbn,
                year_published, publisher, location_id, librarian_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['author'],
                form_data['isbn'], form_data['year_published'], form_data['publisher'],
                request.user.librarian.id, form_data["location"]))

        return redirect(reverse('libraryapp:books'))