import Ember from 'ember';
import convert from 'athena/helpers/units';

/**
 * Return the abbreviated form of the unit for the given measurement type
 * @method unitsUnit
 * @param system {String} Unit system id
 * @param type {String} Type of measurement
 * @return {String} Unit abbreviation
 */
export function unitsUnit(system, type) {
	return convert(system, type).unit;
}

export default Ember.Handlebars.makeBoundHelper(unitsUnit);
