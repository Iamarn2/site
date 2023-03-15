from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    introduction = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
#        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"



class BlockQuote(StructBlock):
    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")

    class Meta:
        icon = "fa-quote-left"



# StreamBlocks
class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph", template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Вставьте URL-адрес для встраивания e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="fa-s15",

    )

# Для блока с изображением и подписью к нему
class AnswerBlock(StructBlock):
    answer_text = CharBlock(label="Вопрос")
    heading_answer = CharBlock(label="Heading для аккардиона", unique=True)
    collapse_answer = CharBlock(label="Collapse для аккардиона", unique=True)
    question_text = RichTextBlock(label="Ответ")
    image_block = ImageChooserBlock(label="Изображение")
    image_caption = CharBlock(label="Подпись изображения")
    image_source = CharBlock(label="Источник изображения")

class AnswerQuestionBlock(StreamBlock):
    answer = AnswerBlock(icon="help", label="Вопрос/Ответ")




