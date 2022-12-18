from .models import Category


def subject_renderer(request):
    return {
        'categories': Category.objects.all()
    }
