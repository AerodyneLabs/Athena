import Ember from 'ember';

var lengthFactors = {
  cm: 100.0,
  m: 1.0,
  km: 0.001,
  in: 39.3701,
  ft: 3.28084,
  mi: 0.000621371,
  nm: 0.000539957
};

export function convertLength(value, unit) {
  var factor = lengthFactors[unit] || NaN;
  return Number(value) * factor;
}

export default Ember.Handlebars.makeBoundHelper(convertLength);
