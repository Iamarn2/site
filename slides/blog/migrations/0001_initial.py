# Generated by Django 4.1.4 on 2023-03-15 17:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.routable_page.models
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailmetadata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0083_workflowcontenttype"),
        ("taggit", "0005_auto_20220424_2025"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=250)),
                ("slug", models.SlugField(max_length=80, unique=True)),
                ("color", models.CharField(blank=True, max_length=20)),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="PostPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("header_image_alt", models.CharField(blank=True, max_length=50)),
                ("header_image_source", models.CharField(blank=True, max_length=250)),
                ("hero_image_alt", models.CharField(blank=True, max_length=50)),
                ("hero_image_source", models.CharField(blank=True, max_length=250)),
                ("teaser", models.CharField(blank=True, max_length=200)),
                ("reading_time", models.CharField(blank=True, max_length=50)),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "intro_text",
                                wagtail.blocks.CharBlock(icon="bold", label="Введение"),
                            ),
                            ("h1", wagtail.blocks.CharBlock(label="H1")),
                            ("h2", wagtail.blocks.CharBlock(label="H2")),
                            ("h4", wagtail.blocks.CharBlock(label="H4")),
                            ("h4_plus", wagtail.blocks.CharBlock(label="H4 Плюсы")),
                            ("h4_minus", wagtail.blocks.CharBlock(label="H4 Минусы")),
                            (
                                "paragraph",
                                wagtail.blocks.RichTextBlock(label="Параграф"),
                            ),
                            (
                                "bullet_list",
                                wagtail.blocks.ListBlock(
                                    wagtail.blocks.CharBlock(label="Пункт списка"),
                                    icon="list-ul",
                                    label="Список",
                                ),
                            ),
                            (
                                "image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image_block",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                label="Изображение"
                                            ),
                                        ),
                                        (
                                            "image_caption",
                                            wagtail.blocks.CharBlock(label="Подпись"),
                                        ),
                                        (
                                            "image_source",
                                            wagtail.blocks.CharBlock(label="Источник"),
                                        ),
                                    ],
                                    icon="image",
                                    label="Изображение",
                                ),
                            ),
                            (
                                "image_carousel",
                                wagtail.blocks.ListBlock(
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Изображение"
                                    ),
                                    icon="image",
                                    label="Карусель",
                                ),
                            ),
                            (
                                "carousel",
                                wagtail.blocks.ListBlock(
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "image_block",
                                                wagtail.images.blocks.ImageChooserBlock(
                                                    label="Изображение"
                                                ),
                                            ),
                                            (
                                                "image_caption",
                                                wagtail.blocks.CharBlock(
                                                    label="Подпись"
                                                ),
                                            ),
                                            (
                                                "image_source",
                                                wagtail.blocks.CharBlock(
                                                    label="Источник"
                                                ),
                                            ),
                                        ],
                                        label="Блок с изображением",
                                    ),
                                    icon="image",
                                    label="Карусель2",
                                ),
                            ),
                            (
                                "video",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "video_image_preview",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                label="Изображение для превью"
                                            ),
                                        ),
                                        (
                                            "video_image_caption",
                                            wagtail.blocks.CharBlock(
                                                label="Название изображения"
                                            ),
                                        ),
                                        (
                                            "video_image_source",
                                            wagtail.blocks.CharBlock(
                                                label="Источник изображения"
                                            ),
                                        ),
                                        (
                                            "video_url",
                                            wagtail.blocks.CharBlock(
                                                label="Ccылка на видео", required=False
                                            ),
                                        ),
                                        (
                                            "video_caption",
                                            wagtail.blocks.CharBlock(
                                                label="Название видео"
                                            ),
                                        ),
                                        (
                                            "video_source",
                                            wagtail.blocks.CharBlock(
                                                label="Источник видео"
                                            ),
                                        ),
                                    ],
                                    icon="media",
                                    label="Видео/Ресурс",
                                ),
                            ),
                            (
                                "video_upload",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "video_image_preview",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                label="Изображение для превью"
                                            ),
                                        ),
                                        (
                                            "video_image_caption",
                                            wagtail.blocks.CharBlock(
                                                label="Название изображения"
                                            ),
                                        ),
                                        (
                                            "video_image_source",
                                            wagtail.blocks.CharBlock(
                                                label="Источник изображения"
                                            ),
                                        ),
                                        (
                                            "video_document",
                                            wagtail.documents.blocks.DocumentChooserBlock(
                                                label="Видео файл", required=False
                                            ),
                                        ),
                                        (
                                            "video_caption",
                                            wagtail.blocks.CharBlock(
                                                label="Название видео"
                                            ),
                                        ),
                                        (
                                            "video_source",
                                            wagtail.blocks.CharBlock(
                                                label="Источник видео"
                                            ),
                                        ),
                                    ],
                                    icon="media",
                                    label="Видео/Документ",
                                ),
                            ),
                            (
                                "quote",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "quotes",
                                            wagtail.blocks.RichTextBlock(
                                                label="Текст цитаты"
                                            ),
                                        ),
                                        (
                                            "quote_by",
                                            wagtail.blocks.CharBlock(
                                                label="Автор цитаты"
                                            ),
                                        ),
                                        (
                                            "quote_by_position",
                                            wagtail.blocks.CharBlock(
                                                label="Должность/Описание автора"
                                            ),
                                        ),
                                        (
                                            "avatar",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                label="Фото автора"
                                            ),
                                        ),
                                        (
                                            "avarar_source",
                                            wagtail.blocks.CharBlock(
                                                label="Источник фото для аватарки"
                                            ),
                                        ),
                                        (
                                            "quotes_source",
                                            wagtail.blocks.CharBlock(
                                                label="Источник цитаты"
                                            ),
                                        ),
                                    ],
                                    icon="openquote",
                                    label="Цитата",
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "post_date",
                    models.DateTimeField(
                        default=datetime.datetime.today, verbose_name="post date"
                    ),
                ),
                (
                    "header_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("taggit.tag",),
        ),
        migrations.CreateModel(
            name="PostPageTags",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_tags",
                        to="blog.postpage",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_items",
                        to="taggit.tag",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="postpage",
            name="tags",
            field=modelcluster.contrib.taggit.ClusterTaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="blog.PostPageTags",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.CreateModel(
            name="Blogpage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=250)),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="PostPageBlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "blog_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_pages",
                        to="blog.blogcategory",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categories",
                        to="blog.postpage",
                    ),
                ),
            ],
            options={
                "unique_together": {("page", "blog_category")},
            },
        ),
    ]