import Ember from 'ember';
import convert from 'athena/helpers/units';

export function unitsValue(system, type, value) {
  return convert(system, type, value).value;
}

export default Ember.Handlebars.makeBoundHelper(unitsValue);
