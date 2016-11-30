from __future__ import unicode_literals

from django.db import models

class Gig(models.Model):
    """
    A model representing a gig and the people going to it.
    """

    act_name = models.CharField(max_length=50,
                                help_text="The name of the act.")

    gig_url = models.URLField(help_text="Website with details of the gig.")

    gig_venue = models.CharField(max_length=50,
                                 help_text="The venue for the gig.")

    gig_time = models.TimeField(help_text="The time of the gig.")

    gig_date = models.DateField(help_text="The date of the gig.")

    meeting_point = models.CharField(max_length=50, blank=True,
                                     help_text="Enter a meeing point (optional).")

    attendees = models.TextField(max_length=500, blank=True,
                                 help_text="Enter attendees here (optional).")

    def __str__(self):
        return self.act_name