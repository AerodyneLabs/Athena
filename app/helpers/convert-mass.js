import Ember from 'ember';

var massFactors = {
  g: 1000.0,
  kg: 1.0,
  oz: 35.274,
  lb: 2.20462
};

export function convertMass(value, unit) {
  var factor = massFactors[unit] || NaN;
  return Number(value) * factor;
}

export default Ember.Handlebars.makeBoundHelper(convertMass);
