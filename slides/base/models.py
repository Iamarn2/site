from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.panels import (FieldPanel, FieldRowPanel, InlinePanel,
                                  MultiFieldPanel, PublishingPanel)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtail.fields import RichTextField, StreamField
from wagtail.models import (Collection, DraftStateMixin, Page,
                            PreviewableMixin, RevisionMixin, Orderable)
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.core import blocks
from rest_framework import serializers
from rest_framework.fields import Field
from wagtail.api import APIField
from .blocks import BaseStreamBlock, AnswerQuestionBlock
from wagtailmetadata.models import MetadataPageMixin


class ImageSerializedField(Field):
    """Serialized для image"""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            'id': value.id,
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }

class HeroCtaLinkSerializer(Field):
    def to_representation(self, page):
        return {
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
        }

# Для вывода дочерних страниц
#https://learnwagtail.com/tutorials/headless-cms-serializing-child-pages-and-querysets/
class HomeChildPagesSerializer(Field):
    def to_representation(self, child_pages):
        return_pages = []
        for child in child_pages:
            post_dict = {
                'id': child.id,
                'title': child.title,
                'slug': child.slug,
                'url': child.url,
            }
            return_pages.append(post_dict)
        return return_pages


    featured_section_1_title = models.CharField(
        blank=True, max_length=50,
    )
    featured_section_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Дополнительный раздел",
    )

class FeaturedSection(models.Model):

    featured_section_name = models.CharField(
        blank=True, max_length=50,
    )
    featured_section_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    add_featured_section = ParentalKey(
        "base.HomePage",
        on_delete=models.CASCADE,
        related_name="add_featured_section"
    )

    api_fields = [
        APIField('featured_section_name'),
        APIField('featured_section_link'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("featured_section_name", heading="Название"),
                FieldPanel("featured_section_link", heading="Ссылка"),
            ],
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title_section

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

# Главная (домашняя) страница
class HomePage(MetadataPageMixin, Page):

    max_count = 1
    
    # Раздел Hero

    image_bg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение фона",
    )
    image_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )
    hero_text_1 = models.CharField(
        max_length=255, help_text="Подзаголовок 1 строка "
    )

    hero_text_2 = models.CharField(
        max_length=255, blank=False, help_text="Подзаголовок 2 строка"
    )

    hero_cta = models.CharField(
        verbose_name="Призыв к действию",
        max_length=255,
        help_text="Текст призыва к действию",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Ссылка для призыва к действию",
        help_text="Выберите страницу для ссылки на призыв к действию",
    )

    # Раздел Услуги

    image_service_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_4 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_5 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_6 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_7 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_service_8 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    # Раздел До/После

    image_before_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    api_fields = [
        APIField('image_bg'),
        APIField('image_1'),
        APIField('image_2'),
        APIField('image_3'),
        APIField('hero_text_1'),
        APIField('hero_text_2'),
        APIField('hero_cta'),
        APIField('hero_cta_link', serializer=HeroCtaLinkSerializer()),
        APIField('image_service_1'),
        APIField('image_service_2'),
        APIField('image_service_3'),
        APIField('image_service_4'),
        APIField('image_service_5'),
        APIField('image_service_6'),
        APIField('image_service_7'),
        APIField('image_service_8'),
        APIField('image_before_1'),
        APIField('image_after_1'),
        APIField('image_before_2'),
        APIField('image_after_2'),
        APIField('image_before_3'),
        APIField('image_after_3'),
        APIField("pages", serializer=HomeChildPagesSerializer(source='get_child_pages')),
        APIField('add_featured_section'),
    ]

    @property
    def get_child_pages(self):
        return self.get_children().public().live()
        # return self.get_children().public().live().values("id", "title", "slug")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image_bg"),
                FieldPanel("image_1"),
                FieldPanel("image_2"),
                FieldPanel("image_3"),
                FieldPanel("hero_text_1", classname="full"),
                FieldPanel("hero_text_2", classname="full"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta"),
                        FieldPanel("hero_cta_link"),
                    ]
                ),
            ],
            heading="Hero раздел",
        ),
        MultiFieldPanel(
            [
                FieldPanel("image_service_1"),
                FieldPanel("image_service_2"),
                FieldPanel("image_service_3"),
                FieldPanel("image_service_4"),
                FieldPanel("image_service_5"),
                FieldPanel("image_service_6"),
                FieldPanel("image_service_7"),
                FieldPanel("image_service_8"),
            ],
            heading="Изображение для сервисов",
        ),
        MultiFieldPanel(
            [
                FieldPanel("image_before_1"),
                FieldPanel("image_after_1"),
                FieldPanel("image_before_2"),
                FieldPanel("image_after_2"),
                FieldPanel("image_before_3"),
                FieldPanel("image_after_3"),
            ],
            heading="Изображение для До/После",
        ),
        MultiFieldPanel([
            InlinePanel("add_featured_section", min_num=1, max_num=20),
        ], heading="Дополнительный раздел"),

    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Домашняя страница"
        verbose_name_plural = "Домашние страницы"

# V Наши услуги (2 вариант с готовыми 6-тью блоками в админке)
class ServicesPage(MetadataPageMixin, Page):

    template = "base/services_page.html"

   # Тип работы 1
    title_1 = models.CharField(
        blank=True, max_length=255
    )
    subtitle_1 = models.CharField(
        blank=True, max_length=255
    )

    text_1 = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

   # Тип работы 2
    title_2 = models.CharField(
        blank=True, max_length=255
    )
    subtitle_2 = models.CharField(
        blank=True, max_length=255
    )

    text_2 = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

   # Тип работы 3
    title_3 = models.CharField(
        blank=True, max_length=255
    )
    subtitle_3 = models.CharField(
        blank=True, max_length=255
    )

    text_3 = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

   # Тип работы 4
    title_4 = models.CharField(
        blank=True, max_length=255
    )
    subtitle_4 = models.CharField(
        blank=True, max_length=255
    )

    text_4 = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image_4 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

   # Тип работы 5
    title_5 = models.CharField(
        blank=True, max_length=255
    )
    subtitle_5 = models.CharField(
        blank=True, max_length=255
    )

    text_5 = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image_5 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

   # Тип работы 6
    title_6 = models.CharField(
        blank=True, max_length=255
    )
    subtitle_6 = models.CharField(
        blank=True, max_length=255
    )

    text_6 = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image_6 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    api_fields = [
        APIField('title_1'),
        APIField('subtitle_1'),
        APIField('text_1'),
        APIField('image-1'),
        APIField('title_2'),
        APIField('subtitle_2'),
        APIField('text_2'),
        APIField('image-2'),
        APIField('title_3'),
        APIField('subtitle_3'),
        APIField('text_3'),
        APIField('image-3'),
        APIField('title_4'),
        APIField('subtitle_4'),
        APIField('text_4'),
        APIField('image-4'),
        APIField('title_5'),
        APIField('subtitle_5'),
        APIField('text_5'),
        APIField('image-5'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("title_1", heading='Тип работы'),
                FieldPanel("subtitle_1", heading='Подзаголовок'),
                FieldPanel("text_1", heading='Описание'),
                FieldPanel("image_1", heading='Изображение'),
            ],heading="Тип услуг 1",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_2", heading='Тип работы'),
                FieldPanel("subtitle_2", heading='Подзаголовок'),
                FieldPanel("text_2", heading='Описание'),
                FieldPanel("image_2", heading='Изображение'),
            ],heading="Тип услуг 2",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_3", heading='Тип работы'),
                FieldPanel("subtitle_3", heading='Подзаголовок'),
                FieldPanel("text_3", heading='Описание'),
                FieldPanel("image_3", heading='Изображение'),
            ],heading="Тип услуг 3",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_4", heading='Тип работы'),
                FieldPanel("subtitle_4", heading='Подзаголовок'),
                FieldPanel("text_4", heading='Описание'),
                FieldPanel("image_4", heading='Изображение'),
            ],heading="Тип услуг 4",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_5", heading='Тип работы'),
                FieldPanel("subtitle_5", heading='Подзаголовок'),
                FieldPanel("text_5", heading='Описание'),
                FieldPanel("image_5", heading='Изображение'),
            ],heading="Тип услуг 5",
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница Наши услуги"
        verbose_name_plural = "Страницы Наши услуги"


# Модель Тип работы
class Option(MetadataPageMixin, RevisionMixin, models.Model):

    title = models.CharField(
        blank=True, max_length=100
    )
    subtitle = models.CharField(
        blank=True, max_length=100
    )

    text = RichTextField(
        null=True, blank=True, max_length=500
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    add_example = ParentalKey(
        "base.OptionsPage",
        on_delete=models.CASCADE,
        related_name="add_example"
    )

    api_fields = [
        APIField('title'),
        APIField('subtitle'),
        APIField('text'),
        APIField('image'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title", heading='Название'),
                FieldPanel("subtitle", heading='Подзаголовок'),
                FieldPanel("text", heading='Описание'),
                FieldPanel("image", heading='Изображение'),
            ],
            classname="collapsible",
        ),

    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Типы работ"
        verbose_name_plural = "Типы работ"

# Страница Типы работ
class OptionsPage(MetadataPageMixin, Page):

    api_fields = [
        APIField('add_example'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("add_example", min_num=0, max_num=20),
        ], heading="Типы работ"),
    ]

    class Meta:
        verbose_name = "Страница Типы работ"
        verbose_name_plural = "Страницы Типы работ"

# До/После  (добавление блоков в админке через ParentalKey)

class After(MetadataPageMixin, RevisionMixin, models.Model):
    # До/После
    title = models.CharField(
        blank=True, max_length=255
    )
    title_1 = models.CharField(
        blank=True, max_length=255
    )
    introduction_1 = models.TextField(blank=True)
    image_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    title_2 = models.CharField(
        blank=True, max_length=255
    )
    introduction_2 = models.TextField(blank=True)
    image_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    add_example = ParentalKey(
        "base.AftersPage",
        on_delete=models.CASCADE,
        related_name="add_example"
    )

    api_fields = [
        APIField('title'),
        APIField('image_1'),
        APIField('title_1'),
        APIField('introduction_1'),
        APIField('image_2'),
        APIField('title_2'),
        APIField('introduction_2'),
    ]

    panels = [
        FieldPanel("title", heading='Заголовок для работы'),
        MultiFieldPanel(
            [
                FieldPanel("image_1", heading='Изображение'),
                FieldPanel("title_1", heading='Заголовок'),
                FieldPanel("introduction_1", heading='Описание'),
            ],
            heading="До изменений",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("image_2", heading='Изображение'),
                FieldPanel("title_2", heading='Заголовок'),
                FieldPanel("introduction_2", heading='Описание'),
            ],
            heading="После изменений",
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пример До/После"
        verbose_name_plural = "Примеры До/После"

class AftersPage(MetadataPageMixin, Page):

    subtitle = models.CharField(
        blank=True, max_length=255
    )

    # Раздел До/После

    image_before_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_4 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_4 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_5 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_5 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_6 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_6 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_7 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_7 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_8 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_8 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_9 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_9 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_before_10 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    image_after_10 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение",
    )

    api_fields = [
        APIField('subtitle'),
        APIField('add_example'),
        APIField("image_before_1"),
        APIField("image_after_1"),
        APIField("image_before_2"),
        APIField("image_after_2"),
        APIField("image_before_3"),
        APIField("image_after_3"),
        APIField("image_before_4"),
        APIField("image_after_4"),
        APIField("image_before_5"),
        APIField("image_after_5"),
        APIField("image_before_6"),
        APIField("image_after_6"),
        APIField("image_before_7"),
        APIField("image_after_7"),
        APIField("image_before_8"),
        APIField("image_after_8"),
        APIField("image_before_9"),
        APIField("image_after_9"),
        APIField("image_before_10"),
        APIField("image_after_10"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("subtitle", heading='Подзаголовок'),
        MultiFieldPanel([
            InlinePanel("add_example", label="пример", min_num=0, max_num=20),
        ], heading="Примеры До/После"),
        MultiFieldPanel(
            [
                FieldPanel("image_before_1"),
                FieldPanel("image_after_1"),
                FieldPanel("image_before_2"),
                FieldPanel("image_after_2"),
                FieldPanel("image_before_3"),
                FieldPanel("image_after_3"),
                FieldPanel("image_before_4"),
                FieldPanel("image_after_4"),
                FieldPanel("image_before_5"),
                FieldPanel("image_after_5"),
                FieldPanel("image_before_6"),
                FieldPanel("image_after_6"),
                FieldPanel("image_before_7"),
                FieldPanel("image_after_7"),
                FieldPanel("image_before_8"),
                FieldPanel("image_after_8"),
                FieldPanel("image_before_9"),
                FieldPanel("image_after_9"),
                FieldPanel("image_before_10"),
                FieldPanel("image_after_10"),
            ],
            heading="Изображение для До/После",
        ),
    ]

    class Meta:
        verbose_name = "Страница До/После"
        verbose_name_plural = "Страницы До/После"

# V Шаги (добавление блоков в админке через ParentalKey)

class Step(MetadataPageMixin, RevisionMixin, models.Model):

    # Тип работы 1
    title = models.CharField(
        blank=True, max_length=255
    )
    subtitle = models.CharField(
        blank=True, max_length=255
    )

    text = RichTextField(
        null=True, blank=True, max_length=1000
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    add_step = ParentalKey(
        "base.StepsPage",
        on_delete=models.CASCADE,
        related_name="add_step"
    )

    api_fields = [
        APIField('title'),
        APIField('subtitle'),
        APIField('text'),
        APIField('image'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title", heading='Заголовок'),
                FieldPanel("subtitle", heading='Подзаголовок (шаг №)'),
                FieldPanel("text", heading='Описание'),
                FieldPanel("image", heading='Изображение'),
            ],
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"

class StepsPage(Page):

    api_fields = [
        APIField('add_step'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("add_step", label="шаг", min_num=1, max_num=7),
        ], heading="Шаги"),
    ]

    class Meta:
        verbose_name = "Страница Шаги"
        verbose_name_plural = "Страницы Шаги"
'''
# V Вопрос/Ответ (добавление блоков в админке через ParentalKey)

class Answer(models.Model):

    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=500)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    image_alt = models.CharField(null=True, blank=True, max_length=50)

    image_source = models.CharField(max_length=250, blank=True)

    add_answer = ParentalKey(
        "base.AnswersPage",
        on_delete=models.CASCADE,
        related_name="add_answer"
    )

    api_fields = [
        APIField('question'),
        APIField('answer'),
        APIField('image'),
        APIField('image_alt'),
        APIField('image_source'),
    ]        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    api_fields = [

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("question", heading="Вопрос"),
                FieldPanel("answer", heading="Ответ"),
                MultiFieldPanel(
                    [
                        FieldPanel("image", heading="Изображение"),
                        FieldPanel("image_alt", heading="Название"),
                        FieldPanel("image_source", heading="Источник"),
                    ], classname="collapsible", heading="Изображение",
                ),
            ], classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопрос-ответ"

class AnswersPage(Page):

    api_fields = [
        APIField('add_answer'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("add_answer", label="вопрос", min_num=1, max_num=20),
        ], heading="Вопрос/Ответ"),
    ]

    class Meta:
        verbose_name = "Страница Вопросы/Ответы"
        verbose_name_plural = "Страницы Вопросы/Ответы"
'''

# Вопрос/Ответ

class AnswerQuestionPage(MetadataPageMixin, Page):
    description = models.CharField(max_length=250, blank=True)
    variants = StreamField(AnswerQuestionBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("description", heading="Вводный текст"),
        FieldPanel("variants", heading="Варианты вопросов"),
    ]

    class Meta:
        verbose_name = "Страница F.A.Q"
        verbose_name_plural = "Страницы F.A.Q"

# V Модель Призыв к действию CTA

class CallsPage(Page):

    introduction = RichTextField(
        null=True, blank=True, max_length=500
    )

    text_cta = models.CharField(
        verbose_name="Призыв к действию",
        max_length=255,
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
        APIField('title'),
        APIField('introduction'),
        APIField('text_cta'),
        APIField('cta_link'),
        APIField('image'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("introduction", heading='Описание'),
                MultiFieldPanel(
                    [
                        FieldPanel("text_cta", heading='Текст призыва к действию'),
                        FieldPanel("cta_link", heading='Ссылка для призыва к действию'),
                    ]
                ),
                FieldPanel("image", heading='Изображение'),
            ],
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница Призыв к действию"
        verbose_name_plural = "Страницы Призывы к действию"

# Стандартная страница

class StandardPage(MetadataPageMixin, Page):
    """
    Общая страница контента. На этом демонстрационном сайте мы используем его для страницы о нас, но
     его можно использовать для любого типа содержимого страницы, которому нужен только заголовок,
     изображение, введение и поле тела
    """

    introduction = models.TextField(help_text="Текст описания страницы", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Только ландшафтный режим; ширина по горизонтали от 1000 до 3000 px",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Содержание страницы", blank=True, use_json_field=True
    )

    api_fields = [
        APIField('introduction'),
        APIField('body'),
        APIField('image'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Стандартная страница"
        verbose_name_plural = "Стандартные страницы"

# Модель Контакты

# Стандартная страница

class GalleryPage(MetadataPageMixin, Page):

    introduction = models.TextField(help_text="Текст описания страницы", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница для галереи"
        verbose_name_plural = "Страницы для галереи"


# https://www.youtube.com/watch?v=kAblCAxsWzY&t=727s
class FormField(AbstractFormField):
    """
     Wagtailforms — это модуль для добавления простых форм на сайт Wagtail. Это
     предназначен не для замены поддержки форм Django, а как быстрый способ
     для создания универсальной формы сбора данных или контактной формы
     без необходимости писать код. Мы используем его на сайте для контактной формы. Ты
     подробнее о формах трясогузки можно прочитать здесь:
    https://docs.wagtail.org/en/stable/reference/contrib/forms/index.html
    """

    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)

# Страница Контакты
class FormPage(AbstractEmailForm):
    subtitle = models.CharField(
        blank=True, max_length=100
    )

    image_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    image_2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    image_3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    image_cta = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    body = StreamField(BaseStreamBlock(), use_json_field=True)
    thank_you_text = RichTextField(blank=True)

    api_fields = [
        APIField('subtitle'),
        APIField('body'),
        APIField('image_1'),
        APIField('image_2'),
        APIField('image_3'),
        APIField('image_cta'),
        APIField('form_fields'),
        APIField('thank_you_text'),
        APIField('from_address'),
        APIField('to_address'),
        APIField('subject'),
    ]

    # Обратите внимание, как мы подключаем объект FormField через InlinePanel с помощью
    # from_address - адрес сервера эл. почты
    # to_address - мой адрес
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("image_1"),
        FieldPanel("image_2"),
        FieldPanel("image_3"),
        FieldPanel("image_cta"),
        InlinePanel("form_fields", label="Поля формы"),
        FieldPanel("thank_you_text", classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Настройки Email",
        ),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница Контакты"
        verbose_name_plural = "Страницы Контакты"

    def get_form_fields(self):
        return self.form_fields.all()


# V Модель Текст для Footer
class FooterText(DraftStateMixin, RevisionMixin, PreviewableMixin, models.Model):
    """
    Это обеспечивает редактируемый текст для нижнего колонтитула сайта. Опять же, он использует декоратор
     `register_snippet`, чтобы он был доступен через администратора. Это сделано
     доступный в шаблоне через тег шаблона, определенный в base/templatetags/navigation_tags.py
    """

    body = RichTextField()

    api_fields = [
        APIField('body'),
    ]

    panels = [
        FieldPanel("body", heading='Текст'),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer сайта"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta:
        verbose_name = "Текст для Footer"
        verbose_name_plural = "Текст для Footer"

class Category(models.Model):

    category_image = models.CharField(max_length=30)

    add_category = ParentalKey(
        "base.PortfolioPage",
        on_delete=models.CASCADE,
        related_name="add_category"
    )

    api_fields = [
        APIField('category_image'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("category_image", heading="Категория"),
            ],
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class PortfolioPage(MetadataPageMixin, Page):

    api_fields = [
        APIField('add_category'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("add_category", min_num=1, max_num=20),
        ], heading="Категории"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница Портфолио"
        verbose_name_plural = "Страницы Портфолио"


class MenuSection(models.Model):


    title_section = models.CharField(
        verbose_name="Название",
        max_length=255,
    )

    section_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    section_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    add_section = ParentalKey(
        "base.MenuPage",
        on_delete=models.CASCADE,
        related_name="add_section"
    )

    api_fields = [
        APIField('title_section'),
        APIField('section_link'),
        APIField('section_image'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title_section", heading="Название"),
                FieldPanel("section_link", heading="Ссылка"),
                FieldPanel("section_image", heading="Изображение"),
            ],
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title_section

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

class MenuPage(Page):

    template = "includes/menu_page.html"

    logo_text = models.CharField(
        max_length=30,
    )

    logo_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    logo_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    button_text = models.CharField(
        verbose_name="Название",
        max_length=50,
    )

    button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


    api_fields = [
        APIField('logo_text'),
        APIField('logo_link'),
        APIField('logo_image'),
        APIField('add_section'),
        APIField('button_text'),
        APIField('button_link'),
   ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("logo_text", heading="Текст"),
            FieldPanel("logo_link", heading="Ссылка"),
            FieldPanel("logo_image", heading="Изображение"),
        ], heading="ЛОГО"),
        MultiFieldPanel([
            InlinePanel("add_section", min_num=1, max_num=20),
        ], heading="ПУНКТЫ МЕНЮ"),
        MultiFieldPanel([
            FieldPanel("button_text", heading="Текст"),
            FieldPanel("button_link", heading="Ссылка"),
        ], heading="КНОПКА"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница Меню"
        verbose_name_plural = "Страницы Меню"


# Цены

class PricePage(MetadataPageMixin, Page):
    description = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description", heading="Вводный текст"),
    ]

    class Meta:
        verbose_name = "Страница Цены"
        verbose_name_plural = "Страницы Цены"
