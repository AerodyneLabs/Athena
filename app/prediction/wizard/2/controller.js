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
  gasTypeError: false,
  balloonError: false,
  payloadMassError: false,
  inputValueError: false,
  needs: ['application', 'prediction/wizard'],
  units: Ember.computed.alias('controllers.application.units'),
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.1');
    },
    next: function() {
      if(this.validate()) {
        this.transitionToRoute('prediction.wizard.3');
      }
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
  }.property('inputType'),
  validate: function() {
    var valid = true;

    var gases = this.get('gases');
    var gas = this.get('gas');
    if(gases.indexOf(gas) < 0) {
      valid = false;
      this.set('gasTypeError', true);
    } else {
      this.set('gasTypeError', false);
    }

    var balloons = this.get('balloons');
    var balloon = this.get('balloon');
    if(balloons.indexOf(balloon) < 0) {
      valid = false;
      this.set('balloonError', true);
    } else {
      this.set('balloonError', false);
    }

    var mass = parseFloat(this.get('payloadMass'));
    if(isNaN(mass) || mass <= 0) {
      valid = false;
      this.set('payloadMassError', true);
    } else {
      this.set('payloadMassError', false);
    }

    var types = this.get('inputOptions');
    var type = this.get('inputType');
    var value = parseFloat(this.get('inputValue'));
    if(types.indexOf(type) < 0 || isNaN(value) || value <= 0) {
      valid = false;
      this.set('inputValueError', true);
    } else {
      this.set('inputValueError', false);
    }

    return valid;
  }
});
