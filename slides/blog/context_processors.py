#from wagtail.core.models import Site
from wagtail.models import Site
from slides.blog.models import Blogpage


def blog_page(request):
    """
    To avoid multiple Wagtail site query in request-response cycle, you can use
    wagtail.contrib.legacy.sitemiddleware.SiteMiddleware
    """
    wagtail_site = Site.find_for_request(request)
    context = {
        'blog_page': Blogpage.objects.in_site(wagtail_site).first()
    }
    return context
