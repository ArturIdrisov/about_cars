from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView 
from django.contrib.auth import logout, login 
from django.views.generic.edit import FormView


from .forms import *
from .models import *
from .utils import *

menu = [{'title': 'About site', 'url_name': 'about'}, 
        {'title': 'Add article', 'url_name': 'add_page'}, 
        {'title': 'Feedback', 'url_name': 'contact'}, 
        {'title': 'Login', 'url_name': 'login'}
]


class AutomobileHome(DataMixin, ListView):
    model = Automobile
    template_name = 'automobile/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(c_def.items())) 

    def get_queryset(self):
        return Automobile.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Automobile.objects.all()
#     cats = Category.objects.all()

#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0, 
#     }

#     return render(request, 'automobile/index.html', context=context)

def about(request):
    contact_list = Automobile.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'automobile/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'About site'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'automobile/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exeption = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Adding an article")
        return dict(list(context.items()) + list(c_def.items())) 

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'automobile/addpage.html', {'form': form, 'menu': menu, 'title': 'Adding an article'})

# def contact(request):
#     return HttpResponse('Feedback')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'automobile/contact.html'
    success_url = reverse_lazy('home')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))
 
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse('Authorization')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')

# def show_post(request, post_slug):
#     post = get_object_or_404(Automobile, slug=post_slug)

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }

#     return render(request, 'automobile/post.html', context=context)  

class ShowPost(DataMixin, DetailView):
    model = Automobile
    template_name = 'automobile/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items())) 
        


class AutomobileCategory(DataMixin, ListView):
    model = Automobile
    template_name = 'automobile/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Automobile.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items())) 

# def show_category(request, cat_id):
#     posts = Automobile.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Display by category',
#         'cat_selected': cat_id, 
#     }

#     return render(request, 'automobile/index.html', context=context) 

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'automobile/login.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'automobile/register.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authorization")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
