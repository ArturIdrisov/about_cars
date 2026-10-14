from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormView

from .forms import AddPostForm, ContactForm, LoginUserForm, RegisterUserForm
from .models import Automobile, Category
from .utils import DataMixin, MENU


class AutomobileHome(DataMixin, ListView):
    model = Automobile
    template_name = "automobile/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Automobile.objects.filter(is_published=True).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Main page"))
        return context


def about(request):
    car_list = Automobile.objects.all()
    paginator = Paginator(car_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "automobile/about.html",
        {"page_obj": page_obj, "menu": MENU, "title": "About site"},
    )


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "automobile/addpage.html"
    success_url = "/"
    login_url = "/login/"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Adding an article"))
        return context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = "automobile/contact.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Feedback"))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("home")


class ShowPost(DataMixin, DetailView):
    model = Automobile
    template_name = "automobile/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title=str(context["post"])))
        return context


class AutomobileCategory(DataMixin, ListView):
    model = Automobile
    template_name = "automobile/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Automobile.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs["cat_slug"])
        context.update(self.get_user_context(title=f"Category - {category.name}", cat_selected=category.pk))
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "automobile/register.html"
    success_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Registration"))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "automobile/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Authorization"))
        return context

    def get_success_url(self):
        return "/"


def logout_user(request):
    logout(request)
    return redirect("login")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
