from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Gig
from .forms import GigForm
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

def index(request):
    """
    Return a list of current gigs to the index page.
    Filter out those more than 7 days old.
    """
    days_threshold = timezone.now() - timedelta(days=settings.FILTER_DAYS)
    gig_list = Gig.objects.filter(gig_date__gt=days_threshold)
    gig_list = gig_list.order_by('gig_date')

    return render_to_response("gigs/index.html", { 
            "gig_list": gig_list,
            })

def add_edit_gig(request, gig_id=None, template_name='gigs/gig.html'):
    """
    Add/Edit gigs.
    """

    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('gigs:index'))
    if gig_id:
        gig = get_object_or_404(Gig, pk=gig_id)
    else:
        gig = Gig()

    form = GigForm(request.POST or None, instance=gig)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gigs:index'))

    return render(request, template_name, context={'form': form})

class GigDelete(DeleteView):
    """
    Delete a gig
    """
    model = Gig
    success_url = reverse_lazy('gigs:index')
    template_name = 'gigs/delete_gig.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse('gigs:index'))
        else:
            return super(GigDelete, self).post(request, *args, **kwargs)