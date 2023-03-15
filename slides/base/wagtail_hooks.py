from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from slides.base.models import FooterText, After, Step

"""
Стайлгайд в настройках:
INSTALLED_APPS = (добавл.'wagtail.contrib.styleguide',)
Здесь же можно найти доступный набор иконок font-awesome. Варианты на https://fontawesome.com/icons.
"""

# Модель Шаги в админке


class StepAdmin(ModelAdmin):
    model = Step
    menu_label = "Шаги"
    menu_icon = "fa-pie-chart"
    list_display = ("title", "subtitle", "text", "image")
    search_fields = ("title",)

# Модель До/После в админке


class AfterAdmin(ModelAdmin):
    model = After
    menu_label = "До/После"
    menu_icon = "fa-files-o"
    list_display = ("title", "image_2")
    search_fields = ("title",)

# Модель Текст в Footer в админке


class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ("body",)

# Модели в главном меню админки


class SlidesModelAdminGroup(ModelAdminGroup):
    menu_label = ""
    menu_icon = "fa-cutlery"
    menu_order = 300  # 4-е место (000 1-е, 100 2-е)
    items = (AfterAdmin, StepAdmin, FooterTextAdmin)


# Добавление группового пункта в главное меню админки
# modeladmin_register(SlidesModelAdminGroup)
