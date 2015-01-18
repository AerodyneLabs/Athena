import Ember from 'ember';
import convert from 'athena/helpers/units';

export function unitsFull(system, type, value) {
  var conv = convert(system, type, value);
  return conv.value + ' ' + conv.unit;
}

export default Ember.Handlebars.makeBoundHelper(unitsFull);
