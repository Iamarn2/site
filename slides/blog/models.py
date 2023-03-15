from django.conf import settings

from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from wagtail.core.models import Page
from wagtail.admin.panels import MultiFieldPanel
#from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.admin.panels import FieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.tags import ClusterTaggableManager
# Блоки для содержимого поста
from .blocks import Body_block
#from wagtail.core.fields import StreamField, RichTextField
from wagtail.fields import StreamField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import datetime
from django.http import Http404
from django.utils.functional import cached_property
from wagtail.api import APIField
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtailmetadata.models import MetadataPageMixin
from django.utils.translation import gettext as _
from allauth.account.forms import LoginForm


'''
class FormField(AbstractFormField):
    page =  ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")

class FormPage(AbstractForm):
    content_panels = AbstractForm.content_panels + [
        InlinePanel("form_fields", label="Field Form")
    ]

    @cached_property
    def blogpage(self):
        return self.get_parent().specific
    
    def get_context(self, request, *args, **kwargs):
        context = super(FormPage, self).get_context(request, *args, **kwargs)
        context ["blogpage"] = self.blogpage
        return context
'''

class Blogpage(MetadataPageMixin, RoutablePageMixin, Page):
    description = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description", heading="Описание"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blogpage"] = self
        # Пагинация
        pagenator = Paginator(self.posts, 4)
        page = request.GET.get("page")
        try:
            posts = pagenator.page(page)
        except PageNotAnInteger:
            posts = pagenator.page(1)
        except EmptyPage:
            posts = pagenator.object_list.none()
        context["posts"] = posts

        return context

    # получить все потомки - опубликованные статьи, отсортированные по дате публикации
    def get_posts(self):
        return PostPage.objects.descendant_of(self).live().order_by("-post_date")

    # маршрутизация по году, месяцу и дню публикации статьи (поста)
    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.search_type = 'date'
        self.search_term = year
        self.posts = self.get_posts().filter(post_date__year=year)

        if month:
            df = DateFormat(datetime.date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
            self.posts = self.posts.filter(post_date__month=month)
        if day:
            self.search_term = date_format(datetime.date(int(year), int(month), int(day)))
            self.posts = self.posts.filter(post_date__day=day)

        return self.render(request)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        postpage = self.get_posts().filter(slug=slug).first()
        if not postpage:
            raise Http404
        return postpage.serve(request)

    # маршрутизация статей по тэгам и категориям
    #    self.posts = self.get_posts().filter(tags__slug=tag)
    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag):
        self.filter_term = tag
        self.filter_type = "тегу"
        self.posts = self.get_posts().filter(tags__slug=tag)
        return self.render(request)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.filter_term = category
        self.filter_type = "категории"
        self.posts = self.get_posts().filter(categories__blog_category__slug=category)
        return self.render(request)

    # маршрутизация для списка статей
    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return self.render(request)

    @route(r'^search/$')
    def post_search(self, request):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.filter_term = search_query
            self.filter_type = "по словам"
            self.posts = self.posts.search(search_query)
        return self.render(request)

    def get_sitemap_urls(self, request=None):
        output = []
        posts = self.get_posts()
        for post in posts:
            post_date = post.post_date
            url = self.get_full_url(request) + self.reverse_subpage(
                'post_by_date_slug',
                args=(
                    post_date.year,
                    '{0:02}'.format(post_date.month),
                    '{0:02}'.format(post_date.day),
                    post.slug,
                )
            )

            output.append({
                'location': url,
                'lastmod': post.last_published_at
            })

        return output

# Страница поста (с выбором категории и добавлением тегов)
class PostPage (MetadataPageMixin,Page):
    header_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    header_image_alt = models.CharField(max_length=50, blank=True)
    header_image_source = models.CharField(max_length=250, blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    hero_image_alt = models.CharField(max_length=50, blank=True)
    hero_image_source = models.CharField(max_length=250, blank=True)
    tags = ClusterTaggableManager(through="PostPageTags", blank=True)
    teaser = models.CharField(max_length=200, blank=True)
    reading_time = models.CharField(max_length=50, blank=True)
    body = StreamField(Body_block(), blank=True, use_json_field=True)
    post_date = models.DateTimeField(verbose_name="post date", default=datetime.datetime.today)

    

    content_panels = Page.content_panels + [
        # ImageChooserPanel("header_image"),
        MultiFieldPanel(
            [
                FieldPanel("header_image", heading="Изображение"),
                FieldPanel("header_image_alt", heading="Подпись"),
                FieldPanel("header_image_source", heading="Источник"),
            ], heading="Изображение для списка статей",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_image", heading="Изображение"),
                FieldPanel("hero_image_alt", heading="Подпись"),
                FieldPanel("hero_image_source", heading="Источник"),
            ], heading="Изображение для Hero",
        ),
        FieldPanel("teaser", heading="Тизер статьи"),
        FieldPanel("reading_time", heading="Длительность чтения", help_text='Образец: 5 минут чтения'),
        FieldPanel("tags", heading="Теги"),
        InlinePanel("categories", label="category", heading="Категории"),
        # StreamFieldPanel("body"),
        FieldPanel("body", heading="Контент"),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel("post_date", heading="Дата создания"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("teaser"),
        index.SearchField("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blogpage"] = self.blogpage

        return context

    @cached_property
    def blogpage(self):
        return self.get_parent().specific

    @cached_property
    def cananical_url(self):
        from .templatetags.blogapp_tags import post_page_date_slug_url
        blogpage = self.blogpage
        return post_page_date_slug_url(self, blogpage)

    def get_sitemap_urls(self, request=None):
        return []

    # для комментариев
    def get_absolute_url(self):
        return self.get_url()

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, 'blog/post_page.html')
        response.context_data['login_form'] = LoginForm()
        return response

# Связываем сниппеты Категории (BlogCategory) со страницей поста
class PostPageBlogCategory(models.Model):
    page = ParentalKey("blog.PostPage", on_delete=models.CASCADE,
                       blank=True, related_name="categories")
    blog_category = models.ForeignKey(
        "blog.BlogCategory", on_delete=models.CASCADE, related_name="post_pages")

    panels = [
        FieldPanel("blog_category", heading="Категории блога"),
    ]

    class Meta:
        unique_together=("page", "blog_category")

# Связываем теги со страницей поста
class PostPageTags(TaggedItemBase):
    content_object = ParentalKey(
        "PostPage", blank=True, related_name="post_tags")

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=80, unique=True)
    color = models.CharField(max_length=20, blank=True)

    panels = [
        FieldPanel("name", heading="Название"),
        FieldPanel("slug", heading="Slug"),
        FieldPanel("color", heading="Цвет категории",
            help_text="Пример: info(голубой), primary(сиреневый), secondary(серый), success(зеленый), danger(красный), warning(желтый)"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


