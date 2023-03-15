from django.contrib import admin
from .models import BlogCategory, Tag
from .models import BlogCategory, Tag, PostPage

#admin.site.register(BlogCategory, BlogCategoryAdmin)

#from taggit.models import Tag as TaggitTag

#admin.site.register(Tag, TagAdmin)
#admin.site.register(Tag, TaggitTagAdmin)

#class TaggitTagAdmin(TranslationAdmin):
#   model = TaggitTag

#@register(TaggitTag)
#class TagAdmin(TranslationAdmin):
#    model = Tag
#class TaggitTagTranslationOptions(TranslationOptions):
#    fields = ('name',)
#translator.register (TaggitTag, TaggitTagTranslationOptions)