import Ember from 'ember';

export function convertTemperature(value, unit, inverse) {
  var val = Number(value);
  if(unit === 'K') {
    return val;
  } else if(unit === 'C') {
    if(inverse) {
      return val + 273.15;
    } else {
      return val - 273.15;
    }
  } else if(unit === 'R') {
    if(inverse) {
      return val / 1.8;
    } else {
      return val * 1.8;
    }
  } else if(unit === 'F') {
    if(inverse) {
      return (value + 459.67) / 1.8;
    } else {
      return (value * 1.8) - 459.67;
    }
  } else {
    return NaN;
  }
}

export default Ember.Handlebars.makeBoundHelper(convertTemperature);
