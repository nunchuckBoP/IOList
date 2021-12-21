
class NextUrlMixin(object):
    request = None    
    success_url = None
    def get_success_url(self):
        return_url = self.request.GET.get('next', None)
        if return_url: return return_url
        else: return self.success_url

    def get_context_data(self, **kwargs):
        context = super(NextUrlMixin, self).get_context_data(**kwargs)
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context
