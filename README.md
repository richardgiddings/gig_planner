# README #

An application designed to show gigs and who is attending. Lets you add, edit, and delete gigs. 

An API is available by adding /api/ to the URL. Uses Django Rest Framework and GET, OPTIONS only
are available to non authorised users.

Currently requires:

- A (Postgres) database to store the gigs.
- bootstrap3_datetime https://github.com/nkunihiko/django-bootstrap3-datetimepicker
- pytz
- djangorestframework
- djangorestframework-jsonp (for padded json)