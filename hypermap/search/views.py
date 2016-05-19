# from django.shortcuts import render

# Create your views here.

import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from pycsw import server


@csrf_exempt
def csw_global_dispatch(request):
    """pycsw wrapper"""

# TODO: add logic for authentication/authorization
#
#    msg = None
#    if any(word in request.body for word in ['Harvest ', 'Transaction ']):
#        if not SOME_AUTHENTICATED_TEST:
#            msg = 'Not authenticated'
#        if not SOME_AUTHORIZATION_TEST:
#            msg = 'Not authorized'
#
#        if msg is not None:
#            template = loader.get_template('search/csw-2.0.2-exception.xml')
#            context = RequestContext(request, {
#                'exception_text': msg
#            })
#            return HttpResponseForbidden(template.render(context), content_type='application/xml')

    env = request.META.copy()
    env.update({'local.app_root': os.path.dirname(__file__),
                'REQUEST_URI': request.build_absolute_uri()})

    csw = server.Csw(settings.PYCSW, env, version='2.0.2')

    content = csw.dispatch_wsgi()

    # pycsw 2.0 has an API break:
    # pycsw < 2.0: content = xml_response
    # pycsw >= 2.0: content = [http_status_code, content]
    # deal with the API break

    if isinstance(content, list):  # pycsw 2.0+
        content = content[1]

    return HttpResponse(content, content_type=csw.contenttype)
