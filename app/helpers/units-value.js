import Ember from 'ember';

export function unitsValue(system, type, value) {
  var val = Number(value);
  var out = val;
  if(type === 'altitude') {
    out = system === 'metric' ? val : val * 3.28084;
  } else if(type === 'temperature') {
    out = system === 'metric' ? val - 273.15 : ((val - 273.15) * 1.8) + 32.0;
  } else if(type === 'distance') {
    out = system === 'metric' ? (val / 1000.0) : (val * 0.000621371);
  } else if(type === 'pressure') {
    out = system === 'metric' ? (val) : (val * 0.000145037738);
  } else if(type === 'lowSpeed') {
    out = system === 'metric' ? (val) : (val * 196.850394);
  } else if(type === 'highSpeed') {
    out = system === 'metric' ? (val * 3.6) : (val * 2.23694);
  }
  return out;
}

export default Ember.Handlebars.makeBoundHelper(unitsValue);
