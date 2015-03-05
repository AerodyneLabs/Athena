import Ember from 'ember';

var speedFactors = {
  'm/s': 1.0,
  kph: 3.6,
  fpm: 196.850394,
  mph: 2.23694,
  kts: 1.94384
};

export function convertSpeed(value, unit, inverse) {
  var factor = speedFactors[unit] || NaN;
  if(inverse) {
    factor = 1.0 / factor;
  }
  return Number(value) * factor;
}

export default Ember.Handlebars.makeBoundHelper(convertSpeed);
