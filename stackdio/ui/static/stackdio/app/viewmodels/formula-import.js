/*!
  * Copyright 2014,  Digital Reasoning
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

define([
    'jquery',
    'knockout',
    'ladda',
    'bootbox',
    'utils/utils',
    'select2'
], function ($, ko, Ladda, bootbox, utils) {
    'use strict';

    return function() {
        var self = this;

        self.breadcrumbs = [
            {
                active: false,
                title: 'Formulas',
                href: '/formulas/'
            },
            {
                active: true,
                title: 'Import'
            }
        ];


        // View variables
        self.uri = ko.observable();
        self.username = ko.observable();
        self.password = ko.observable();
        self.accessToken = ko.observable();
        self.usernameText = ko.observable();

        self.subscription = null;

        self.repos = ko.observableArray([]);
        self.selectedRepo = ko.observable();

        self.loadRepos = function () {
            $.ajax({
                method: 'GET',
                url: 'https://api.github.com/orgs/stackdio-formulas/repos'
            }).done(function (repos) {
                self.repos(repos.sort(function (a, b) {
                    return a.name < b.name ? -1 : a.name > b.name ? 1 : 0;
                }));
            }).fail(function () {
                utils.growlAlert('GitHub API rate limit exceeded.  Could not load default set ' +
                    'of formulas.  Please enter the full url instead.', 'warning')
            });
        };

        // Necessary functions
        self.reset = function() {
            self.uri('');
            self.username('');
            self.password('');

            self.accessToken.subscribe(function (newVal) {
                if (newVal) {
                    self.usernameText('GitHub access token');
                } else {
                    self.usernameText('Git username');
                }
            });

            self.accessToken(false);

            // Change the url when
            self.selectedRepo.subscribe(function (newVal) {
                if (newVal) {
                    self.uri(newVal.clone_url);
                }
            });
        };

        self.removeErrors = function(keys) {
            keys.forEach(function (key) {
                var el = $('#' + key);
                el.removeClass('has-error');
                var help = el.find('.help-block');
                help.remove();
            });
        };

        self.importFormula = function() {
            // First remove all the old error messages
            var keys = ['uri', 'username', 'password', 'access_token'];

            self.removeErrors(keys);

            // Grab both button objects
            var importButton = Ladda.create(document.querySelector('#import-button'));

            // Start them up
            importButton.start();

            // Create the formula!
            $.ajax({
                'method': 'POST',
                'url': '/api/formulas/',
                'data': JSON.stringify({
                    uri: self.uri(),
                    git_username: self.username(),
                    git_password: self.password(),
                    access_token: self.accessToken()
                })
            }).always(function () {
                // Stop our spinning buttons FIRST
                importButton.stop();
            }).done(function () {
                // Successful creation - just redirect to the main formulas page
                window.location = '/formulas/';
            }).fail(function (jqxhr) {
                // Display any error messages
                var message = '';
                try {
                    var resp = JSON.parse(jqxhr.responseText);
                    for (var key in resp) {
                        if (resp.hasOwnProperty(key)) {
                            if (keys.indexOf(key) >= 0) {
                                var el = $('#' + key);
                                el.addClass('has-error');
                                resp[key].forEach(function (errMsg) {
                                    el.append('<span class="help-block">' + errMsg + '</span>');
                                });
                            } else if (key === 'non_field_errors') {
                                resp[key].forEach(function (errMsg) {
                                    if (errMsg.indexOf('uri') >= 0) {
                                        var el = $('#uri');
                                        el.addClass('has-error');
                                        el.append('<span class="help-block">A formula with this URI already exists.</span>');
                                    }
                                });
                            } else {
                                var betterKey = key.replace('_', ' ');

                                resp[key].forEach(function (errMsg) {
                                    message += '<dt>' + betterKey + '</dt><dd>' + errMsg + '</dd>';
                                });
                            }
                        }
                    }
                    if (message) {
                        message = '<dl class="dl-horizontal">' + message + '</dl>';
                    }
                } catch (e) {
                    message = 'Oops... there was a server error.  This has been reported to ' +
                        'your administrators.';
                }
                if (message) {
                    bootbox.alert({
                        title: 'Error importing formula',
                        message: message
                    });
                }
            });
        };

        self.reset();
        self.loadRepos();
    };
});
