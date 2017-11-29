({
    appDir: 'stackdio/ui/static/stackdio/app',
    baseUrl: '.',
    dir: 'stackdio/ui/static/stackdio/build',
    modules: [
        {
            name: 'main',
            include: [
                'bloodhound',
                'bootbox',
                'bootstrap',
                'cookie',
                'domReady',
                'fuelux',
                'jquery',
                'knockout',
                'ladda',
                'moment',
                'select2',
                'spin',
                'typeahead',
                'underscore',
                'utils/mobile-fix',
                'utils/class',
                'utils/utils',
                'utils/bootstrap-growl',
                'generics/pagination',
            ]
        }
    ]
})