import re
from slides.blog.models import Tag, BlogCategory
#from slides.blog.md_converter.utils import render_markdown
from django.template import Library, loader
from urllib.parse import urlparse, urlunparse
from django.http import QueryDict

register = Library()

# 5
# список категорий для страницы списка постов blog_page.html


@register.inclusion_tag("blog/components/main_categories.html", takes_context=True)
def category_list(context):
    categories = BlogCategory.objects.all()
    return {
        "request": context["request"],
        "blogpage": context["blogpage"],
        "categories": categories
    }
# список тегов для страницы списка постов blog_page.html


@register.inclusion_tag("blog/components/main_tags.html", takes_context=True)
def tag_list(context):
    tags = Tag.objects.all()
    return {
        "request": context["request"],
        "blogpage": context["blogpage"],
        "tags": tags
    }


@register.inclusion_tag("blog/components/post_tags.html", takes_context=True)
def post_tag_list(context):
    page = context["page"]
    post_tags = page.tags.all()
    return {
        "request": context["request"],
        "blogpage": context["blogpage"],
        "post_tags": post_tags
    }


@register.inclusion_tag("blog/components/post_categories.html", takes_context=True)
def post_categories_list(context):
    page = context["page"]
    post_categories = page.categories.all()
    return {
        "request": context["request"],
        "blogpage": context["blogpage"],
        "post_categories": post_categories
    }


@register.simple_tag()
def post_page_date_slug_url(postpage, blogpage):
    post_date = postpage.post_date
    url = blogpage.full_url + blogpage.reverse_subpage(
        "post_by_date_slug",
        args=(
            post_date.year,
            "{0:02}".format(post_date.month),
            "{0:02}".format(post_date.day),
            postpage.slug,
        )
    )
    return url


@register.filter(name="embedurl")
def get_embed_url_with_parameters(url):
    if "youtube.com" in url or "youtu.be" in url:
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"  # Get video id from URL
        embed_url = re.sub(
            regex, r"https://www.youtube.com/embed/\1", url
        )  # Append video id to desired URL
        print(embed_url)
        embed_url_with_parameters = embed_url + "?rel=0"  # Add additional parameters
        return embed_url_with_parameters
    else:
        return None


'''
@register.filter(name='markdown')
def markdown(value):
    return render_markdown(value)
'''


@register.simple_tag
def url_replace(request, **kwargs):
    """
    This tag can help us replace or add querystring
    TO replace the page field in URL
    {% url_replace request page=page_num %}
    """
    (scheme, netloc, path, params, query, fragment) = urlparse(request.get_full_path())
    query_dict = QueryDict(query, mutable=True)
    for key, value in kwargs.items():
        query_dict[key] = value
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))
