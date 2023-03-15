from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    ListBlock,
    TextBlock,
)
from django.db import models
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
#from wagtailmarkdown.blocks import MarkdownBlock





# Для блока с цитатой
class QuoteBlock(StructBlock):
    quotes = RichTextBlock(label="Текст цитаты")
    quote_by = CharBlock(label="Автор цитаты")
    quote_by_position = CharBlock(label="Должность/Описание автора")
    avatar = ImageChooserBlock(label="Фото автора")
    avarar_source = CharBlock(label="Источник фото для аватарки")
    quotes_source = CharBlock(label="Источник цитаты")

# Для блока с изображением и подписью к нему
class ImageBlock(StructBlock):
    image_block = ImageChooserBlock(label="Изображение")
    image_caption = CharBlock(label="Подпись")
    image_source = CharBlock(label="Источник")

# Для блока с видео и подписью к нему
#video_url = CharBlock(label="Ccылка на видео")
#video = EmbedBlock(label="Видео")
class VideoBlock(StructBlock):
    video_image_preview = ImageChooserBlock(label="Изображение для превью")
    video_image_caption = CharBlock(label="Название изображения")
    video_image_source = CharBlock(label="Источник изображения")
    video_url = CharBlock(required=False, label="Ccылка на видео")
    video_caption = CharBlock(label="Название видео")
    video_source = CharBlock(label="Источник видео")
#    video_upload = models.ForeignKey(
#       'wagtaildocs.Document', blank=True, null=True,
#        on_delete=models.SET_NULL, related_name='+'
#   )
#   video_upload = DocumentChooserBlock(required=False, label="Видео файл")
class VideoUploadBlock(StructBlock):
    video_image_preview = ImageChooserBlock(label="Изображение для превью")
    video_image_caption = CharBlock(label="Название изображения")
    video_image_source = CharBlock(label="Источник изображения")
    video_document = DocumentChooserBlock(required=False, label="Видео файл")
    video_caption = CharBlock(label="Название видео")
    video_source = CharBlock(label="Источник видео")

class PersonBlock(StructBlock):
    first_name = CharBlock()
    surname = CharBlock()
    photo = ImageChooserBlock(required=False)
    photo_source = CharBlock(label="Источник фото")
    biography = RichTextBlock()


class CarouselBlock(StructBlock):
    image_block = ImageChooserBlock(label="Изображение")
    image_caption = CharBlock(label="Подпись")
    image_source = CharBlock(label="Источник")


# Общий класс со всеми видами блоков
# markdown = MarkdownBlock(icon="code")
class Body_block(StreamBlock):
    intro_text = CharBlock(icon="bold", label="Введение")
    h1 = CharBlock(label="H1")
    h2 = CharBlock(label="H2")
    h4 = CharBlock(label="H4")
    h4_plus = CharBlock(label="H4 Плюсы")
    h4_minus = CharBlock(label="H4 Минусы")
    paragraph = RichTextBlock(label="Параграф")
    bullet_list = ListBlock(CharBlock(label="Пункт списка"),icon="list-ul", label="Список")
    image = ImageBlock(icon="image", label="Изображение")
    image_carousel = ListBlock(ImageChooserBlock(label="Изображение",), label="Карусель", icon="image")
    carousel = ListBlock(CarouselBlock(label="Блок с изображением"), label="Карусель2", icon="image")
    video = VideoBlock(icon="media", label="Видео/Ресурс")
    video_upload = VideoUploadBlock(icon="media", label="Видео/Документ")
    quote = QuoteBlock(icon="openquote", label="Цитата")
