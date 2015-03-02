import Ember from 'ember';

export default Ember.ObjectController.extend({
  needs: ['application'],
  units: Ember.computed.alias('controllers.application.units')
});
