import Ember from 'ember';

export default Ember.Controller.extend({
  units: 'metric',

  unitsOptions: [{
    id: 'imperial',
    name: 'Imperial'
  }, {
    id: 'metric',
    name: 'Metric'
  }]
});
