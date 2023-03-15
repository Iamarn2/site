# Generated by Django 4.1.4 on 2023-03-15 17:04

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0083_workflowcontenttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimpleGalleryIndex",
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
                (
                    "intro_title",
                    models.CharField(
                        blank=True,
                        help_text=" H1 для gallery page.",
                        max_length=250,
                        verbose_name="Заголовок вступления",
                    ),
                ),
                (
                    "intro_text",
                    wagtail.fields.RichTextField(blank=True, verbose_name="Текст"),
                ),
                (
                    "images_per_page",
                    models.IntegerField(
                        default=8, verbose_name="Количество изображений на 1 странице"
                    ),
                ),
                (
                    "use_lightbox",
                    models.BooleanField(
                        default=True,
                        help_text="Использовать лайтбокс для просмотра больших изображений при нажатии на миниатюру.",
                        verbose_name="Использовать lightbox",
                    ),
                ),
                (
                    "order_images_by",
                    models.IntegerField(
                        choices=[
                            (1, "Image title"),
                            (2, "Newest image first"),
                            (3, "Image tag"),
                        ],
                        default=3,
                    ),
                ),
                ("title_call", models.CharField(blank=True, max_length=100)),
                (
                    "introduction_1",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "introduction_2",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "introduction_3",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "text_cta",
                    models.CharField(max_length=100, verbose_name="Призыв к действию"),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="Collection",
                    ),
                ),
                (
                    "cta_link",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Страница simple gallery",
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
    ]
