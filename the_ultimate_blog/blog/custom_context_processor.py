from .models import Category, Article
from datetime import timedelta
from django.utils import timezone

some_day_last_week = timezone.now().date() - timedelta(days=7)
monday_of_last_week = some_day_last_week + timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
monday_of_this_week = monday_of_last_week + timedelta(days=7)


def subject_renderer(request):
    return {
        'categories': Category.objects.all(),
        'top_articles': Article.publish.filter(created__gte=monday_of_last_week, created__lt=monday_of_this_week)
        .order_by('-views')[:3],
        'trending_tags': Article.tags.most_common()[:15],


    }
