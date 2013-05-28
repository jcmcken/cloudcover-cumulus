from tastypie.paginator import Paginator
from django.conf import settings
from cumulus.defaults import LIMIT_PER_PAGE

class CumulusPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        # set max limit to something a little more realistic
        kwargs['max_limit'] = getattr(settings, 'API_LIMIT_PER_PAGE', LIMIT_PER_PAGE)

        super(CumulusPaginator, self).__init__(*args, **kwargs)

    def get_limit(self):
        # don't let user pull unlimited records from db
        if self.limit in [0, None]:
            self.limit = getattr(settings, 'API_LIMIT_PER_PAGE', LIMIT_PER_PAGE)
        return super(CumulusPaginator, self).get_limit()

    def page(self):
        # add ``page_number`` to result meta
        output = super(CumulusPaginator, self).page()
        output['meta']['page_number'] = int(self.offset / self.limit) + 1
        return output

