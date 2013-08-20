from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages, auth
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

DEFAULT_REDIRECT = 'index'
APPLICATION_TEMPLATE = 'main_application.html'
LANDING_PAGE_TEMPLATE = 'index.html'

def render(request, view, context={}):
    if (request):
        return render_to_response(view, context, context_instance=RequestContext(request))
    return render_to_response(view, context)

def index(request):
    template = LANDING_PAGE_TEMPLATE
    if request.user.is_authenticated():
        template = APPLICATION_TEMPLATE
    return render(request, template)

def login(request):
    next_url = request.GET.get('next', DEFAULT_REDIRECT)
    if request.method == 'POST':
        un = request.POST.get('username', '')
        pw = request.POST.get('password', '')
        user = auth.authenticate(username=un, password=pw)
        
        if user is not None and user.is_active:
            # Login the user
            auth.login(request, user)
            return redirect(next_url)
        else:
            # Failed
            messages.error(request, 'Login was unsuccessful.  Please try again.')
            return redirect(index)
    else:
        messages.error(request, 'Invalid method \'{0}\' used. Please use '
                                'POST.'.format(request.method))
        return redirect(next_url)

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successfull. You may login again if you wish')
    return redirect('index')
