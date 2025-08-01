from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

admin.site.register(Genre)


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # (tùy chọn) không tạo sẵn dòng trống mới


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    llist_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
