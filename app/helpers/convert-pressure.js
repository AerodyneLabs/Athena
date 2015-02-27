import Ember from 'ember';

var pressureFactors = {
  Pa: 1.0,
  hPa: 0.01,
  mbar: 0.01,
  mmHg: 0.00750061683,
  inHg: 0.000295333727
};

export function convertPressure(value, unit) {
  var factor = pressureFactors[unit] || NaN;
  return Number(value) * factor;
}

export default Ember.Handlebars.makeBoundHelper(convertPressure);
