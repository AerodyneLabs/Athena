import Ember from 'ember';

export function unitsUnit(system, type) {
  var value = '';
  if(type === 'altitude') {
    value = system === 'metric' ? 'm' : 'ft';
  } else if(type === 'temperature') {
    value = system === 'metric' ? 'C' : 'F';
  } else if(type === 'distance') {
    value = system === 'metric' ? 'km' : 'mi';
  } else if(type === 'pressure') {
    value = system === 'metric' ? 'Pa' : 'psi';
  } else if(type === 'lowSpeed') {
    value = system === 'metric' ? 'm/s' : 'fpm';
  } else if(type === 'highSpeed') {
    value = system === 'metric' ? 'kph' : 'mph';
  }
  return value;
}

export default Ember.Handlebars.makeBoundHelper(unitsUnit);
