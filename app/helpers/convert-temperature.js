import Ember from 'ember';

export function convertTemperature(value, unit) {
  var val = Number(value);
  if(unit === 'K') {
    return val;
  } else if(unit === 'C') {
    return val - 273.15;
  } else if(unit === 'R') {
    return val * 1.8;
  } else if(unit === 'F') {
    return (value * 1.8) - 459.67;
  } else {
    return NaN;
  }
}

export default Ember.Handlebars.makeBoundHelper(convertTemperature);
