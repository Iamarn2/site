from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import MultiFieldPanel
#from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.panels import FieldPanel
#from wagtail.fields import RichTextField
from wagtail.fields import RichTextField
#from wagtail.core.models import Page
from wagtail.models import Page
from wagtail.images import get_image_model

from django.shortcuts import render, redirect
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from taggit.models import Tag
from wagtail.api import APIField
from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField

class SimpleGallerySerializer(Field):
    def to_representation(self, value):
        return {
            'id': value.id,
        }


IMAGE_ORDER_TYPES = (
    (1, 'Image title'),
    (2, 'Newest image first'),
    (3, 'Image tag'),
)


class SimpleGalleryIndex(RoutablePageMixin, Page):
    intro_title = models.CharField(
        verbose_name=_('Заголовок вступления'),
        max_length=250,
        blank=True,
        help_text=_(' H1 для gallery page.')
    )
    intro_text = RichTextField(
        blank=True,
        verbose_name=_('Текст'),
    )
    collection = models.ForeignKey(
        'wagtailcore.Collection',
        verbose_name=_('Collection'),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    images_per_page = models.IntegerField(
        default=8,
        verbose_name=_('Количество изображений на 1 странице'),
    )
    use_lightbox = models.BooleanField(
        verbose_name=_('Использовать lightbox'),
        default=True,
        help_text=_('Использовать лайтбокс для просмотра больших изображений при нажатии на миниатюру.')
    )
    order_images_by = models.IntegerField(choices=IMAGE_ORDER_TYPES, default=3)

    # Блок Призыва к действию
 
    title_call = models.CharField(
        blank=True, max_length=100
    )
 
    introduction_1 = models.CharField(
        null=True, blank=True, max_length=200
    )
    introduction_2 = models.CharField(
        null=True, blank=True, max_length=200
    )
    introduction_3 = models.CharField(
        null=True, blank=True, max_length=200
    )
    text_cta = models.CharField(
        verbose_name="Призыв к действию",
        max_length=100,
    )

    cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    api_fields = [
        APIField('intro_title'),
        APIField('intro_text'),
        APIField('collection', serializer=SimpleGallerySerializer()),
        APIField('images_per_page'),
        APIField('use_lightbox'),
        APIField('order_images_by'),
        APIField('title_call'),
        APIField('introduction_1'),
        APIField('introduction_2'),
        APIField('introduction_3'),
        APIField('text_cta'),
        APIField('cta_link'),
        APIField('image'),
    ]


    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('intro_title', classname='full title'),
                FieldPanel('intro_text', classname='full title'),
                FieldPanel('collection'),
                FieldPanel('images_per_page', classname='full title'),
                FieldPanel('use_lightbox'),
                FieldPanel('order_images_by'),
            ],heading="Галерея",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_call", heading='Заголовок призыва'),
                FieldPanel("introduction_1", heading='Начало описания'),
                FieldPanel("introduction_2", heading='Выделенный фрагмент описания'),
                FieldPanel("introduction_3", heading='Окончание описания'),
                MultiFieldPanel(
                    [
                        FieldPanel("text_cta", heading='Текст призыва к действию'),
                        FieldPanel("cta_link", heading='Ссылка для призыва к действию'),
                    ]
                ),
                FieldPanel("image", heading='Изображение'),
            ], heading='Призыв к действию',
            classname="collapsible",
        ),
    ]

    @property
    def images(self, tags=None):
        return get_gallery_images(self.collection.name, self)

    @property
    def tags(self):
        return self.get_gallery_tags()

    def get_context(self, request):
        images = self.images
        tags = self.tags
        context = super(SimpleGalleryIndex, self).get_context(request)
        page = request.GET.get('page')
        paginator = Paginator(images, self.images_per_page)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        context['gallery_images'] = images
        context['gallery_tags'] = tags
        return context


    def get_gallery_tags(self, tags=[]):
        images = get_gallery_images(self.collection.name, self, tags=tags)
        for img in images:
            tags += img.tags.all()
        tags = sorted(set(tags))
        return tags

#    @route('^tags/$', name='tag_archive')
#    @route('^tags/([\w-]+)/$', name='tag_archive')
    @property
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            return redirect(self.url)
        try:
            taglist.append(tag)
        except NameError:
            taglist = []
            taglist.append(tag)

        images = get_gallery_images(self.collection.name, self, tags=taglist)
        tags = self.get_gallery_tags(tags=taglist)
        paginator = Paginator(images, self.images_per_page)
        page = request.GET.get('page')
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        context = self.get_context(request)
        context['gallery_images'] = images
        context['gallery_tags'] = tags
        context['current_tag'] = tag
        return render(request, getattr(settings, 'SIMPLE_GALLERY_TEMPLATE', 'wagtail_simple_gallery/simple_gallery_index.html'), context)

    class Meta:
        verbose_name = _(getattr(settings, 'SIMPLE_GALLERY_PAGE_TYPE', 'Страница simple gallery'))

    template = getattr(settings, 'SIMPLE_GALLERY_TEMPLATE', 'wagtail_simple_gallery/simple_gallery_index.html')


def get_gallery_images(collection, page=None, tags=None):
    # Tags must be a list of tag names like ["Hasthag", "Kawabonga", "Winter is coming"]
    images = None
    try:
        images = get_image_model().objects.filter(collection__name=collection).prefetch_related("tags")
        if page:
            if page.order_images_by == 1:
                images = images.order_by('title')
            elif page.order_images_by == 2:
                images = images.order_by('-created_at')
            elif page.order_images_by == 3:
                images = images.order_by('tags')
    except Exception as e:
        pass
    if images and tags:
        images = images.filter(tags__name__in=tags).prefetch_related("tags").distinct()
    return images
