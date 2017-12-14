/*!
  * Copyright 2017,  Digital Reasoning
  *
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  *
  *     http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  *
*/

{% load staticfiles %}
{# Templatize this file so that the static files always work even if the static url changes #}

requirejs.config({
    baseUrl: '{% static 'stackdio/app' %}',
    paths: {
        'bloodhound': '{% static 'lib/typeahead.js/dist/bloodhound' %}',
        'bootbox': '{% static 'lib/bootbox/bootbox' %}',
        'bootstrap': '{% static 'lib/bootstrap/dist/js/bootstrap' %}',
        'cookie': '{% static 'lib/js-cookie/src/js.cookie' %}',
        'domReady': '{% static 'lib/requirejs-domReady/domReady' %}',
        'fuelux': '{% static 'lib/fuelux/dist/js/fuelux' %}',
        'jquery': '{% static 'lib/jquery/dist/jquery' %}',
        'knockout': '{% static 'lib/knockout/build/output/knockout-latest' %}',
        'ladda': '{% static 'lib/ladda/js/ladda' %}',
        'moment': '{% static 'lib/moment/moment' %}',
        'select2': '{% static 'lib/select2/dist/js/select2' %}',
        'spin': '{% static 'lib/ladda/js/spin' %}',
        'typeahead': '{% static 'lib/typeahead.js/dist/typeahead.jquery' %}',
        'underscore': '{% static 'lib/underscore/underscore' %}'
    },
    shim: {
        bootstrap: {
            deps: ['jquery']
        },
        typeahead: {
            deps: ['jquery'],
            init: function($) {
                // This fixes an issue with typeahead.  Once this typeahead bug is fixed in a
                // future release, this whole typeahead entry in the shim can be removed, but this
                // is robust enough to work with OR without the bugfix.
                var registry = require.s.contexts._.registry;
                if (registry.hasOwnProperty('typeahead.js')) {
                    return registry['typeahead.js'].factory($);
                } else if (registry.hasOwnProperty('typeahead')) {
                    return registry['typeahead'].factory($);
                } else {
                    console.error('Unable to load typeahead.js.');
                }
            }
        }
    }
});

// Add our custom capitalize method
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

require([
    'jquery',
    'cookie',
    'bootstrap',
    'fuelux',
    'utils/mobile-fix',
    'domReady!'
], function($, Cookie) {
    // Check for safe methods
    // pulled from Django 1.9 documentation
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // Grab the CSRF token
    var csrftoken = Cookie.get('csrftoken');

    // Set up some basic jQuery ajax settings globally so we don't have to worry about it later
    $.ajaxSetup({
        contentType: 'application/json',
        headers: {
            'Accept': 'application/json'
        },
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.method) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var advancedWarning = Cookie.get('displayAdvancedWarning');

    if (!window.stackdio.advancedView && typeof advancedWarning === 'undefined') {
        // Save the element
        var $el = $('.stackdio-advanced-warning');

        // Show the message
        $el.removeClass('stackdio-advanced-warning');

        function turnOfWarning(e) {
            Cookie.set('displayAdvancedWarning', false, {expires: 365, path: '/'});
        }

        // Register our click handlers to set the cookie
        $('#advanced-warning-dismiss').click(turnOfWarning);
        $('#advanced-warning-button').click(turnOfWarning)
    }
});
