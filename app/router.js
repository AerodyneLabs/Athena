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

  this.route('navaids');
  this.route('navaid', {
    path: '/navaid/:id'
  });

  this.resource('prediction', {
    path: '/predictions'
  }, function() {
    this.route('detail', {
      path: '/:id'
    });
    this.route('wizard', function() {
      this.route('1');
      this.route('2');
      this.route('3');
      this.route('4');
    });
  });
});

export default Router;
