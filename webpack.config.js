var path = require('path');
var fs = require('fs');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var entryObj = {};

fs.readdirSync('stackdio/ui/static/stackdio/app/viewmodels').forEach(function (file) {
    entryObj[file.substring(0, file.length - 3)] = './viewmodels/' + file;
});

entryObj['main'] = './main.js';

module.exports = {
  context: path.resolve(__dirname, 'stackdio/ui/static/stackdio/app'),

  entry: {
      main: './main.js'
  },

  output: {
      path: path.resolve('stackdio/ui/static/stackdio/bundles/'),
      filename: "[name]-[hash].js"
  },

  plugins: [
    new BundleTracker({filename: 'stackdio/ui/static/stackdio/webpack-stats.json'})
  ],

  module: {},

  resolve: {
    alias: {
        bloodhound: 'typeahead.js/dist/bloodhound',
        bootbox: 'bootbox.js/bootbox',
        cookie: 'js-cookie/src/js.cookie',
        fuelux: 'fuelux/dist/js/fuelux',
        typeahead: 'typeahead.js/dist/typeahead.jquery'
    },
    modules: ['stackdio/ui/static/stackdio/app', 'node_modules'],
    extensions: ['.js', '.jsx']
  }
};
