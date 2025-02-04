from datetime import datetime
from django.db import connection
from django.shortcuts import render
from django.views import View

def my_error_404(request, exception):
    return render(request, 'no_found.html', status=404)

class ModelCrudView(View):
    template_name = ''
    url_page = ''
    url_name_create = ''
    name_bnt_create = ''
    model = None
    criterion = None
    columns_name = []
    columns_model = []
    size_page = 5
    icon_true = 'fa-solid fa-check'
    icon_false = 'fa-solid fa-close'

    class Context:
        def __init__(self,
                     model,
                     criterion,
                     size_page,
                     columns_name,
                     columns_model,
                     url_page,
                     url_name_create,
                     name_bnt_create,
                     icon_true,
                     icon_false
                     ):

            self.query = model.objects
            if criterion is not None:
                self.query = self.query.filter(**criterion)

            self.url_page = url_page
            self.url_name_create = url_name_create
            self.name_bnt_create = name_bnt_create
            self.icon_true = icon_true
            self.icon_false = icon_false
            self.current_page = 0
            self.records = 0
            self.pages = 0
            self.size_page = size_page
            self.range = range(0, size_page)
            self.columns_name = columns_name
            self.columns_model = columns_model
            self.items = []

        def calc_range_pages(self):
            start_range = max(0, self.current_page - 2)
            end_range = min(start_range + self.size_page, self.pages)

            if end_range - start_range < self.size_page:
                start_range = max(0, end_range - self.size_page)

            self.range = range(start_range, end_range)

        def change_page(self, request, next_page=0):
            tenant_schema = request.tenant.schema_name
            self.current_page = int(next_page)
            with connection.schema_editor(tenant_schema):
                self.records = self.query.count()
                self.pages = (self.records - 1) // self.size_page + 1
                self.calc_range_pages()
                start_index = self.current_page * self.size_page
                end_index = start_index + self.size_page
                self.items = list(self.query.order_by('-id')[start_index:end_index])

    def get_context(self, request):
        context = self.Context(
            model=self.model,
            size_page=self.size_page,
            columns_name=self.columns_name,
            columns_model=self.columns_model,
            url_page=self.url_page,
            url_name_create=self.url_name_create,
            name_bnt_create=self.name_bnt_create,
            icon_true=self.icon_true,
            icon_false=self.icon_false,
            criterion=self.criterion
        )
        if 'page' in request.GET:
            context.change_page(request=request, next_page=request.GET.get('page'))
        else:
            context.change_page(request)
        return context

    def get(self, request):
        context = self.get_context(request)
        return render(request=request, template_name=self.template_name, context=context.__dict__)


class DataLink:
    def __init__(self, url_name, title_link, icon, is_active_by_url_name=True, url_pattern=None):
        self.title_link = title_link
        self.icon = icon
        self.url_name = url_name
        self.is_active_by_url_name = is_active_by_url_name
        self.url_pattern = url_pattern


class SectionMenu:
    def __init__(self, title_section: str, links: list[DataLink]):
        self.title_section = title_section
        self.links = links


class MenuSideBaseView(View):
    template_name = ''
    title = ''
    icon = ''
    is_smoke = False
    sections = []

    class Context:
        def __init__(self, title, icon, is_smoke, sections, current_year, current_month):
            self.title = title
            self.icon = icon
            self.is_smoke = is_smoke
            self.sections = sections
            self.current_year = current_year
            self.current_month = current_month

    def get_context(self):
        now = datetime.now()
        return self.Context(
            title=self.title,
            icon=self.icon,
            is_smoke=self.is_smoke,
            sections=self.sections,
            current_year=now.year,
            current_month=now.month,
        ).__dict__

    def get(self, request):
        return render(request=request, template_name=self.template_name, context=self.get_context())
