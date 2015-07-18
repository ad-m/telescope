from django.views.generic import TemplateView
from django.conf import settings
from tors.views import QueryMixin


class BookmarksView(QueryMixin, TemplateView):
    template_name = 'bookmarks/list.html'

    def get_context_data(self, **kwargs):
        context = super(BookmarksView, self).get_context_data(**kwargs)
        queries = {}
        for query in settings.TOR_BOOKMARKS:
            queries[query] = self.manager.query('summary', search=query, limit=5)
        context['queries'] = queries
        return context
