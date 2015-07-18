from onion_py.manager import Manager
from onion_py.caching import OnionSimpleCache
from django.views.generic import TemplateView, FormView
from .forms import SearchForm


class PaginationMixin(object):
    per_page = 10

    def get_page(self):
        return int(self.kwargs.get('page', 0))

    def get_context_data(self, **kwargs):
        context = super(PaginationMixin, self).get_context_data(**kwargs)
        page = self.get_page()
        context['page'] = page
        if page > 0:
            context['prev_page'] = page-1
        context['next_page'] = page+1
        return context


class QueryMixin(object):
    manager = Manager(OnionSimpleCache())
    query = None

    def get_query(self):
        assert self.query is not None
        return self.query

    def get_query_kwargs(self, **kwargs):
        return {'query': self.get_query()}

    def get_query_args(self):
        return []

    def get_queryset(self):
        return self.manager.query(*self.get_query_args(), **self.get_query_kwargs())


class QueryListMixin(QueryMixin):
    query = None

    def get_query_kwargs(self, **kwargs):
        kwargs = super(QueryListMixin, self).get_query_kwargs(**kwargs)
        kwargs.update(dict(limit=self.per_page, offset=self.per_page*self.get_page()))
        return kwargs


class SummaryView(PaginationMixin, QueryListMixin, TemplateView):
    template_name = 'tors/summary.html'
    query = 'summary'

    def get_context_data(self, **kwargs):
        context = super(SummaryView, self).get_context_data(**kwargs)
        context['query'] = self.get_queryset()
        return context


class SearchView(PaginationMixin, QueryListMixin, FormView):
    template_name = 'tors/search.html'
    query = 'summary'
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SearchView, self).get_form_kwargs(**kwargs)
        kwargs['data'] = self.request.GET
        return kwargs

    def get_query_kwargs(self):
        kwargs = super(SearchView, self).get_query_kwargs()
        if self.form.is_valid():
            kwargs['search'] = self.form.cleaned_data['keyword']
        return kwargs

    def form_valid(self, form):
        context = {}
        context['form'] = form
        context['keyword'] = form.cleaned_data['keyword']
        self.form = form
        context['query'] = self.get_queryset()
        return self.render_to_response(self.get_context_data(**context))


class AddressView(PaginationMixin, QueryListMixin, TemplateView):
    template_name = 'tors/summary_address.html'
    query = 'summary'

    def get_context_data(self, **kwargs):
        context = super(AddressView, self).get_context_data(**kwargs)
        context['address'] = self.kwargs['address']
        context['query'] = self.get_queryset()
        return context

    def get_query_kwargs(self, **kwargs):
        kwargs = super(AddressView, self).get_query_kwargs(**kwargs)
        kwargs.update(dict(search=self.kwargs['address']))
        return kwargs


class DetailsView(QueryMixin, TemplateView):
    template_name = 'tors/details.html'
    query = 'details'

    def get_context_data(self, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)
        context['query'] = self.get_queryset()
        return context

    def get_query_kwargs(self, **kwargs):
        kwargs = super(DetailsView, self).get_query_kwargs(**kwargs)
        kwargs.update(dict(lookup=self.kwargs['fingerprint']))
        return kwargs
