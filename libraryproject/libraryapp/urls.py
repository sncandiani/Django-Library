from django.urls import include, path
from .views import *

app_name = "libraryapp"
# defines the urls that the library app will respond to
urlpatterns = [
    # these two patterns are referring to book_list which is available through the init file in views
    path('', home, name='home'),
    path('books/', book_list, name='books'),
    path('librarians/', librarian_list, name='librarians'),
    path('libraries/', library_list, name='libraries'),
    # lets application use the built-in login and logout views that Django provides
    path('accounts/', include('django.contrib.auth.urls')),
    # By default, the Django logout function takes the user to the admin site, must create custom
    path('logout/', logout_user, name='logout'),
    # clients can request books to be added using the book form
    path('book/form', book_form, name='book_form'),
    path('library/form', library_form, name='library_form'), 
    # used to capture any integer that is the route parameter, and stores that number in the book_id variable
    path('books/<int:book_id>/', book_details, name='book'),
    path('library/<int:library_id>/', library_details, name='library'),
    path('librarian/<int:librarian_id>/', librarian_details, name='librarian'), 
    path('books/<int:book_id>/form/', book_edit_form, name='book_edit_form'),
]