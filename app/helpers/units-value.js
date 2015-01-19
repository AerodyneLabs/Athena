import Ember from 'ember';
import convert from 'athena/helpers/units';
import round from 'athena/helpers/round';

export function unitsValue(system, type, value, digits) {
  var out = convert(system, type, value).value;
  if(digits) {
    if(type === 'altitude') {
      if(system === 'metric') {
        return round(out, -2);
      } else {
        return round(out, -1);
      }
    } else if(type === 'temperature') {
      return round(out, -2);
    } else if(type === 'distance') {
      return round(out, -3);
    } else if(type === 'pressure') {
      if(system === 'metric') {
        return round(out, -1);
      } else {
        return round(out, -4);
      }
    } else if(type === 'lowSpeed') {
      return round(out, -2);
    } else if(type === 'highSpeed') {
      return round(out, -1);
    }
  }
  return out;
}

export default Ember.Handlebars.makeBoundHelper(unitsValue);
