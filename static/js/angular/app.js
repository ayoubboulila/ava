'use strict';


// Declare app level module which depends on filters, and services
angular.module('PIRC', [
  'ngRoute',
  'PIRC.filters',
  'PIRC.services',
  'PIRC.directives',
  'PIRC.controllers',
  'angular.circular-slider'
]).
config(['$routeProvider', '$interpolateProvider', function($routeProvider, $interpolateProvider) {
  $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: 'MyCtrl1'});
  $routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: 'MyCtrl2'});
  $routeProvider.otherwise({redirectTo: '/view1'});
  $interpolateProvider.startSymbol('{?');
  $interpolateProvider.endSymbol('?}');
}]);
