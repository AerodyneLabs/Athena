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
  gases: ['Helium', 'Hydrogen'],
  gas: 'Helium',
  payloadMass: 1.0,
  inputOptions: [
    'Ascent Rate',
    'Target Altitude',
    'Net Lift'
  ],
  inputType: 'Ascent Rate',
  inputValue: '',
  needs: ['application', 'prediction/wizard'],
  units: Ember.computed.alias('controllers.application.units'),
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.1');
    },
    next: function() {
      this.transitionToRoute('prediction.wizard.3');
    }
  },
  inputUnit: function() {
    var type = this.get('inputType');
    if(type === 'Ascent Rate') {
      return this.get('units.speed');
    } else if(type === 'Target Altitude') {
      return this.get('units.altitude');
    } else if(type === 'Net Lift') {
      return this.get('units.mass');
    } else {
      return '?';
    }
  }.property('inputType')
});
