import sqlite3 
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Library
from ..connection import Connection

@login_required
def library_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            # changes using row method in order to refer by name, not index
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
            SELECT 
                l.id, 
                l.name, 
                l.address
                from libraryapp_library l;   
            """)
            # establishes empty list 
            all_libraries = []
            dataset = db_cursor.fetchall()
            # for each row assign the following values
            for row in dataset: 
                library = Library()
                library.id = row["id"]
                library.name = row["name"]
                library.address = row["address"]
                all_libraries.append(library)
                # refers to template in templates folder
            template_name = "libraries/list.html"
            # context are the values held in all_libraries list which should be library objects
            context = {
                'all_libraries': all_libraries
            }
        return render(request, template_name, context)
    elif request.method == 'POST': 
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
            INSERT INTO libraryapp_library
            (
                name, address
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['address']))

        return redirect(reverse('libraryapp:libraries'))
