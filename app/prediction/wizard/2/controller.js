import Ember from 'ember';

export default Ember.Controller.extend({
  balloons: [
    'Kaymont 200g',
    'Kaymont 300g',
    'Kaymont 350g',
    'Kaymont 600g',
    'Kaymont 800g',
    'Kaymont 1000g',
    'Kaymont 1200g',
    'Kaymont 1500g',
    'Kaymont 2000g',
    'Kaymont 3000g'
  ],
  balloon: '',
  needs: ['application', 'prediction/wizard'],
  units: Ember.computed.alias('controllers.application.units'),
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.1');
    },
    next: function() {
      this.transitionToRoute('prediction.wizard.3');
    }
  }
});
