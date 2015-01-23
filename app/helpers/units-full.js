import Ember from 'ember';
import convert from 'athena/helpers/units';

/**
 * Convert the value and unit from SI base units
 * @method unitsFull
 * @param system {String} The unit system id
 * @param type {String} The type of measurement
 * @param value {Number} The value to convert
 * @return {String} The full converted measurement
 */
export function unitsFull(system, type, value) {
  var conv = convert(system, type, value);
  return conv.value + ' ' + conv.unit;
}

export default Ember.Handlebars.makeBoundHelper(unitsFull);
