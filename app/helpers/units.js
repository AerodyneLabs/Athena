import Ember from 'ember';

export default function(system, type, value) {
  var val = Number(value || 0);
  var out = {value: val, unit: ''};
  if(type === 'altitude') {
    if(system === 'metric') {
      out.unit = 'm';
      out.value = val;
    } else {
      out.unit = 'ft';
      out.value = val * 3.28084;
    }
  } else if(type === 'temperature') {
    if(system === 'metric') {
      out.unit = new Ember.Handlebars.SafeString('&deg;C');
      out.value = val - 273.15;
    } else {
      out.unit = new Ember.Handlebars.SafeString('&deg;F');
      out.value = ((val - 273.15) * 1.8) + 32.0;
    }
  } else if(type === 'distance') {
    if(system === 'metric') {
      out.unit = 'km';
      out.value = val / 1000.0;
    } else {
      out.unit = 'mi';
      out.value = val * 0.000621371;
    }
  } else if(type === 'pressure') {
    if(system === 'metric') {
      out.unit = 'Pa';
      out.value = val;
    } else {
      out.unit = 'psi';
      out.value = val * 0.000145037738;
    }
  } else if(type === 'lowSpeed') {
    if(system === 'metric') {
      out.unit = 'm/s';
      out.value = val;
    } else {
      out.unit = 'fpm';
      out.value = val * 196.850394;
    }
  } else if(type === 'highSpeed') {
    if(system === 'metric') {
      out.unit = 'kph';
      out.value = val * 3.6;
    } else {
      out.unit = 'mph';
      out.value = val * 2.23694;
    }
  }
  return out;
}
