from asyncio.format_helpers import _format_callback
from calendar import c
from multiprocessing import AuthenticationError
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth import logout, login





class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html/'
    context_object_name = 'posts' # использование имени в шаблонизаторе jinja вместо object_list
    #extra_context = {'title': 'Главна страница'} #изменения названия в вкладке, только статические типы

    def get_context_data(self, *, object_list=None, **kwargs): 
        #функция добавления статического и динамического контекcта в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        #Показывать не все статьи,а фильтровать по только опубликованым
        return Women.objects.filter(is_published=True).select_related('cat')


#def index(request):
    #posts = Women.objects.all()
    #context = {
    #    'posts':posts,
    #    'menu': menu,
     #   'title':'Главная страница',
      #  'cat_selected': 0,
    #}
    #return render(request, 'women/index.html', context=context)

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})



class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs): 
        #функция добавления статического и динамического контекcта в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))
   

#def addpage(request):
 #   if request.method == 'POST':
  #      form = AddPostForm(request.POST, request.FILES) #метод добавления в форму фото
   #     if form.is_valid():
    #        #print(form.cleaned_data)
     #       form.save()
      #      return redirect('home')
    #else:
     #   form = AddPostForm()
    #return render(request, 'women/addpage.html', {
     #   'form': form,
      #  'menu': menu,
       # 'title': 'Добавление статьи'
    #})



class ContactFormViev(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return  c_def | context  #dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
#def login(request):
 #   return HttpResponse('Авторизация')



class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, *, object_list=None, **kwargs): 
        #функция добавления статического и динамического контекcта в шаблон
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

#def show_post(request, post_slug):
 #   post = get_object_or_404(Women, slug=post_slug)

  #  context = {
   #     'post': post,
    #    'menu': menu,
     #      'title': post.title,
      #  'cat_selected': post.cat_id,

    #}
    
    #return render(request, 'women/post.html', context=context)



def pageNotFound(request, exeception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html/'
    context_object_name = 'posts'
    allow_empty = False #404 если нет такой категории

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs): 
        #функция добавления статического и динамического контекcта в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='категория - ' + str(context['posts'][0].cat), cat_selected = context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

#def show_category(request, cat_slug):
    #posts = Women.objects.filter(cat__slug=cat_slug)


    #context = {
    #    'posts':posts,
     #   'menu': menu,
      #  'title':'Отображение по рубрикам',
       # 'cat_selected': cat_slug,
    #}
    #return render(request, 'women/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистриация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'


    def get_context_data(self, *, object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
    
   


def logout_user(request):
    logout(request)
    return redirect('login')
