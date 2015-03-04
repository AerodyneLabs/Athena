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
  liftInput: '',
  rateInput: '',
  altitudeInput: '',
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
  update: function() {
    Ember.run.once(this, 'compute');
  }.observes(
    'balloon',
    'gas',
    'payloadMass',
    'liftInput',
    'rateInput',
    'altitudeInput',
    'units.altitude',
    'units.mass',
    'units.speed'
  ),
  compute: function() {
    var lift = Number(this.get('liftInput'));
    var rate = Number(this.get('rateInput'));
    var alt = Number(this.get('altitudeInput'));
    console.log(lift, rate, alt);
  }
});
