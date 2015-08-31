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
    'generics/pagination',
    'models/host'
], function ($, Pagination, Host) {
    'use strict';

    return Pagination.extend({
        alerts: [],
        breadcrumbs: [
            {
                active: false,
                title: 'Stacks',
                href: '/stacks/'
            },
            {
                active: false,
                title: 'Stack Detail',
                href: '/stacks/' + window.stackdio.stackId + '/'
            },
            {
                active: true,
                title: 'Stack Hosts'
            }
        ],
        autoRefresh: false,
        model: Host,
        baseUrl: '/stacks/',
        initialUrl: '/api/stacks/' + window.stackdio.stackId + '/hosts/',
        sortableFields: [
            {name: 'hostDefinition', displayName: 'Host Type', width: '15%'},
            {name: 'hostname', displayName: 'Hostname', width: '15%'},
            {name: 'fqdn', displayName: 'FQDN', width: '30%'},
            {name: 'privateDNS', displayName: 'Private DNS', width: '15%'},
            {name: 'publicDNS', displayName: 'Public DNS', width: '15%'},
            {name: 'state', displayName: 'State', width: '10%'}
        ]
    });
});
