import random
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.contrib.auth.models import User
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class BulletinsList(ListView):
    model = Bulletin
    template_name = 'bulletins/board.html'
    context_object_name = 'board'
    queryset = Bulletin.objects.order_by('-create_time')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BulFilter(self.request.GET, queryset=self.get_queryset())
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        return context


class BulletinsSearch(ListView):
    model = Bulletin
    template_name = 'bulletins/search.html'
    context_object_name = 'search'
    queryset = Bulletin.objects.order_by('-create_time')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BulWideFilter(self.request.GET, queryset=self.get_queryset())
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        return context


class BulletinDetail(DetailView, CreateView):
    model = Bulletin
    form_class = ReplyForm
    template_name = 'bulletins/bulletin.html'
    context_object_name = 'bulletin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        context['self_bul'] = Bulletin.objects.filter(bul_author=self.request.user)
        context['form'] = ReplyForm()
        context['replies'] = Reply.objects.filter(reply_bul=self.kwargs.get('pk'))
        context['self_replies'] = Reply.objects.filter(reply_bul=self.kwargs.get('pk'),
                                                       reply_user=self.request.user).order_by('-reply_date')
        return context

    def post(self, request, *args, **kwargs):
        reply_text = request.POST['reply_text']
        reps = Reply.objects.filter(reply_user=request.user, reply_bul=Bulletin.objects.get(id=self.kwargs.get('pk')),
                                    reply_date__date=datetime.today()).count()

        if reps < 1:
            newrep = Reply.objects.create(reply_user=request.user,
                                          reply_bul=Bulletin.objects.get(id=self.kwargs.get('pk')),
                                          reply_text=reply_text)
            newrep.save()
            messages.success(request, 'Отклик добавлен!')
        else:
            messages.error(request, 'Сегодня Вы уже оставили отклик на это объявление. Пользователь может оставить '
                                    'только один отклик на каждое объявление в день')

        return super().get(request, *args, **kwargs)


class BulletinCreate(LoginRequiredMixin, CreateView):
    model = Bulletin
    template_name = 'bulletins/create.html'
    form_class = BulletinForm
    context_object_name = 'create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BulletinForm()
        return context

    def post(self, request, *args, **kwargs):
        bul_title = request.POST['bul_title']
        bul_text = request.POST['bul_text']
        category = request.POST['category']
        newbul = Bulletin.objects.create(bul_author=request.user,
                                         bul_title=bul_title, bul_text=bul_text, category=category)

        newbul.save()
        messages.success(request, 'Объявление добавлено успешно!')

        return super().get(request, *args, **kwargs)


class BulletinEdit(LoginRequiredMixin, UpdateView):
    model = Bulletin
    template_name = 'bulletins/edit.html'
    form_class = BulletinForm
    context_object_name = 'edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')

        return Bulletin.objects.get(id=id)


class BulletinDelete(LoginRequiredMixin, DeleteView):
    template_name = 'bulletins/delete.html'
    queryset = Bulletin.objects.all()
    success_url = '/board/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileList(LoginRequiredMixin, ListView):
    model = Bulletin
    template_name = 'profilelist.html'
    context_object_name = 'profilelist'
    queryset = Bulletin.objects.order_by('-create_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BulFilter(self.request.GET, queryset=self.get_queryset())
        self_bul = Bulletin.objects.filter(bul_author=self.request.user)
        context['self_bul'] = self_bul
        return context


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'replies/replies.html'
    context_object_name = 'replies'
    queryset = Reply.objects.order_by('-reply_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ReplyFilter(self.request.GET, queryset=self.get_queryset())
        context['replies'] = Reply.objects.filter(reply_bul__bul_author=self.request.user)
        return context


@login_required
def reply_accept(request, **kwargs):
    rep = Reply.objects.get(id=kwargs.get('pk'))
    rep.accept = True
    rep.save(update_fields=['accept'])
    return redirect('/board/profile/replies')


@login_required
def reply_disaccept(request, **kwargs):
    rep = Reply.objects.get(id=kwargs.get('pk'))
    rep.accept = False
    rep.save(update_fields=['accept'])
    return redirect('/board/profile/replies')


class SelfReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'replies/self_replies.html'
    context_object_name = 'replies'
    queryset = Reply.objects.order_by('-reply_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SelfReplyFilter(self.request.GET, queryset=self.get_queryset())
        context['replies'] = Reply.objects.filter(reply_user=self.request.user)

        return context


class ReplyEdit(LoginRequiredMixin, UpdateView):
    model = Reply
    template_name = 'replies/editrep.html'
    form_class = ReplyForm
    context_object_name = 'editrep'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')

        return Reply.objects.get(id=id)


class ReplyDelete(LoginRequiredMixin, DeleteView):
    template_name = 'replies/deleterep.html'
    queryset = Reply.objects.all()
    success_url = '/board/'


class NewsView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = News.objects.order_by('-create_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        context['is_subscribed'] = Subscribers.objects.filter(subscriber=self.request.user).exists()

        return context


@login_required
def news_subscribe(request):
    Subscribers.objects.create(subscriber=request.user)
    return redirect('/board/news')


@login_required
def news_unsubscribe(request):
    Subscribers.objects.filter(subscriber=request.user).delete()
    return redirect('/board/news')


class NewsDetail(DetailView):
    model = News
    template_name = 'news/new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        return context


class NewsCreate(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/createnews.html'
    form_class = NewsForm
    context_object_name = 'createnews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsForm()
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        return context

    def post(self, request, *args, **kwargs):
        news_title = request.POST['news_title']
        news_text = request.POST['news_text']
        new = News.objects.create(news_author=request.user,
                                  news_title=news_title, news_text=news_text)

        new.save()

        return super().get(request, *args, **kwargs)


class NewsEdit(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'news/editnews.html'
    form_class = NewsForm
    context_object_name = 'editnews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')

        return News.objects.get(id=id)


class NewsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'news/deletenews.html'
    queryset = News.objects.all()
    success_url = '/board/news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = User.objects.filter(id=self.request.user.id, is_staff=True)
        return context

