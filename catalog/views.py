from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Book, Author, BookInstance, Genre
from catalog import constants
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    """View function for home page of site."""
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact=constants.LOAN_STATUS_AVAILABLE).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    template_name = 'books/my_arbitrary_template_name_list.html'
    paginate_by = constants.BOOK_LIST_VIEW_PAGINATE


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = constants.LOAN_BOOKS_BY_USER_LIST_VIEW_PAGINATE

    def get_queryset(self):
        return (
            BookInstance.objects
            .filter(borrower=self.request.user, status__exact=constants.LOAN_STATUS_ON_LOAN)
            .order_by('due_back')
        )


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lấy danh sách các bản sao của cuốn sách
        context['copies'] = self.object.bookinstance_set.all()
        context['genres'] = self.object.genre.all()
        context['STATUS_AVAILABLE'] = constants.LOAN_STATUS_AVAILABLE
        context['STATUS_MAINTENANCE'] = constants.LOAN_STATUS_MAINTENANCE
        return context

@login_required
@permission_required('catalog.can_mark_returned')
def mark_book_returned(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.status = constants.LOAN_STATUS_AVAILABLE
    book_instance.save()
    return redirect('my-borrowed')
