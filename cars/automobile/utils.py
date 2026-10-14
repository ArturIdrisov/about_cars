from django.db.models import Count

from .models import Category

MENU = [
    {"title": "About site", "url_name": "about"},
    {"title": "Add article", "url_name": "add_page"},
    {"title": "Feedback", "url_name": "contact"},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count("automobile"))

        user_menu = MENU.copy()
        if not self.request.user.is_authenticated:
            user_menu = [item for item in user_menu if item["url_name"] != "add_page"]

        context["menu"] = user_menu
        context["cats"] = categories
        context.setdefault("cat_selected", 0)
        return context
