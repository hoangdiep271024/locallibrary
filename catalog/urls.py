from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),  # Trang chủ của app "catalog"
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    path(
        'mybooks/',
        views.LoanedBooksByUserListView.as_view(),
        name='my-borrowed',
    ),
    path(
        'book/<uuid:pk>/return/',
        views.mark_book_returned,
        name='mark-returned',
    ),
    path(
        'book/<uuid:pk>/renew/',
        views.renew_book_librarian,
        name='renew-book-librarian'),
    path(
        'author/create/',
        views.AuthorCreate.as_view(),
        name='author-create'),
    path(
        'author/<int:pk>/update/',
        views.AuthorUpdate.as_view(),
        name='author-update'),
    path(
        'author/<int:pk>/delete/',
        views.AuthorDelete.as_view(),
        name='author-delete'),
]
