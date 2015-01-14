import Ember from 'ember';
import convert from 'athena/helpers/units';

export function unitsUnit(system, type) {
  return convert(system, type).unit;
}

export default Ember.Handlebars.makeBoundHelper(unitsUnit);
