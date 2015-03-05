import Ember from 'ember';

var pressureFactors = {
  Pa: 1.0,
  hPa: 0.01,
  mbar: 0.01,
  mmHg: 0.00750061683,
  inHg: 0.000295333727,
  Psi: 0.000145037738
};

export function convertPressure(value, unit, inverse) {
  var factor = pressureFactors[unit] || NaN;
  if(inverse) {
    factor = 1.0 / factor;
  }
  return Number(value) * factor;
}

export default Ember.Handlebars.makeBoundHelper(convertPressure);
