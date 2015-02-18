import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('about');

  this.route('forecastPeriods');
  this.route('forecastPeriod', {
    path: '/forecastPeriod/:id'
  });

  this.route('soundings');
  this.route('sounding', {
    path: '/sounding/:id'
  });

  this.route('centers');
  this.route('center', {
    path: '/center/:id'
  });

  this.route('flights');
  this.route('flight', {
    path: '/flight/:id'
  });
});

export default Router;
