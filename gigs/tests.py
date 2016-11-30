from django.test import TestCase
from .models import Gig
from django.core.urlresolvers import reverse
from django.utils import timezone

"""
Helper method to add a gig.
"""
def _add_gig(act_name, gig_url, gig_venue, gig_time, gig_date, attendees):

    Gig.objects.create(act_name=act_name, gig_url=gig_url,
                       gig_venue=gig_venue, gig_time=gig_time,
                       gig_date=gig_date, attendees=attendees)


class IndexViewTests(TestCase):

    def test_index_no_gigs(self):
        response = self.client.get(reverse('gigs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gigs/index.html')

    def test_index_with_gig(self):
        _add_gig(
            'Human League', 
            'https://m.ticketmaster.co.uk/event/1F004F828CF62BFB', 
            'Colston Hall', '19:00',
            timezone.now(), 'David Guest Jon Trace Caroline Wilson Kim Dowsett')

        response = self.client.get(reverse('gigs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gigs/index.html')

        self.assertContains(response, '7 p.m.')
        self.assertContains(response, 'Wilson')


class AddViewTests(TestCase):

    def test_adding_a_gig_screen(self):
        response = self.client.get(reverse('gigs:add_gig'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gigs/gig.html')

    def test_adding_a_gig_save(self):
        response = self.client.post(
                reverse('gigs:add_gig'),
                    data={
                    'act_name': 'The Cure', 
                    'gig_url': 'https://m.ticketmaster.co.uk/event/1F004F828CF62BFB',
                    'gig_venue': 'O2 Academy, Bristol', 
                    'gig_time': '20:00',
                    'gig_date': '2016-05-01', 
                    'attendees': 'David Guest Richard Giddings'},
                    follow=True
        )
        self.assertEqual(Gig.objects.count(), 1)
        self.assertQuerysetEqual(response.context['gig_list'],['<Gig: The Cure>'])
        self.assertContains(response, 'Richard Giddings')
        self.assertContains(response, 'O2 Academy, Bristol')

    def test_adding_a_gig_cancel(self):
        response = self.client.post(
                reverse('gigs:add_gig'),
                        data={'cancel': 'Cancel'}, # cancel the add
                        follow=True
        )
        self.assertEqual(Gig.objects.count(), 0)
        self.assertContains(response, 'There are no gigs yet.')    


class EditViewTests(TestCase):

    def setUp(self):
        _add_gig(
            'Human League', 
            'https://m.ticketmaster.co.uk/event/1F004F828CF62BFB', 
            'Colston Hall', '19:00',
            timezone.now(), 'David Guest Jon Trace Caroline Wilson Kim Dowsett')


    def test_editing_a_gig_screen(self):

        gig = Gig.objects.first()

        response = self.client.get(reverse('gigs:edit_gig', args=(gig.id,)))
        self.assertContains(response, 'Human League')
        self.assertContains(response, 'Jon Trace')

    def test_editing_a_gig_save(self):

        gig = Gig.objects.first()
        response = self.client.get(reverse('gigs:edit_gig',
                                            args=(gig.id,)))
        form = response.context['form']
        data = form.initial
        data['act_name'] = 'The Pogues'
        data['gig_date'] = '2016-01-10'

        response = self.client.post(reverse('gigs:edit_gig', 
                                    kwargs={'gig_id': gig.id}), 
                                    data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['gig_list'],['<Gig: The Pogues>'])

    def test_editing_a_gig_cancel(self):

        gig = Gig.objects.first()
        response = self.client.get(reverse('gigs:edit_gig',
                                            args=(gig.id,)))
        form = response.context['form']
        data = form.initial
        data['act_name'] = 'The Pogues'
        data['gig_date'] = '2016-01-10'
        data['cancel'] = 'Cancel' # cancel the edit

        response = self.client.post(reverse('gigs:edit_gig', 
                                    kwargs={'gig_id': gig.id}), 
                                    data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['gig_list'],['<Gig: Human League>'])


class DeleteViewTests(TestCase):

    def test_deleting_a_gig_screen(self):
        _add_gig(
            'Human League', 
            'https://m.ticketmaster.co.uk/event/1F004F828CF62BFB', 
            'Colston Hall', '19:00',
            timezone.now(), 'David Guest Jon Trace Caroline Wilson Kim Dowsett')
        gig = Gig.objects.first()

        response = self.client.get(reverse('gigs:delete_gig', kwargs={'pk': gig.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gigs/delete_gig.html')

    def test_deleting_a_gig_save(self):
        _add_gig(
            'Human League', 
            'https://m.ticketmaster.co.uk/event/1F004F828CF62BFB', 
            'Colston Hall', '19:00',
            timezone.now(), 'David Guest Jon Trace Caroline Wilson Kim Dowsett')
        gig = Gig.objects.first()

        self.assertEqual(Gig.objects.count(), 1)
        response = self.client.post(reverse('gigs:delete_gig', 
                                    kwargs={'pk': gig.id}), follow=True)
        self.assertTemplateUsed(response, 'gigs/index.html')
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Gig.objects.count(), 0)

    def test_deleting_a_gig_cancel(self):
        _add_gig(
            'Human League', 
            'https://m.ticketmaster.co.uk/event/1F004F828CF62BFB', 
            'Colston Hall', '19:00',
            timezone.now(), 'David Guest Jon Trace Caroline Wilson Kim Dowsett')
        gig = Gig.objects.first()

        response = self.client.post(reverse('gigs:delete_gig', 
                                    kwargs={'pk': gig.id}), 
                                    data={'cancel': 'Cancel'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['gig_list'],['<Gig: Human League>'])