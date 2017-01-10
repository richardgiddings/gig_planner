# README #

An application designed to show gigs and who is attending. Lets you add, edit, and delete gigs. 

An API is available by adding /api/ to the URL. Uses Django Rest Framework and GET, OPTIONS only
are available to non authorised users.

Emails sent on ADD/EDIT/DELETE of gig data as a bcc to those people in the settings.BCC_LIST list.

Currently requires:

- A (Postgres) database to store the gigs.
- bootstrap3_datetime https://github.com/nkunihiko/django-bootstrap3-datetimepicker
- pytz
- djangorestframework
- djangorestframework-jsonp (for padded json)