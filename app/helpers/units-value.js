import Ember from 'ember';
import convert from 'athena/helpers/units';
import round from 'athena/helpers/round';

/**
 * Convert and return the value rounded to sensible precision
 * @method unitsValue
 * @param system {String} Unit system id
 * @param type {String} Type of measurement
 * @param value {Number} Value in SI base units
 * @return {Number} Converted value
 */
export function unitsValue(system, type, value) {
	var out = convert(system, type, value).value;
	if (type === 'altitude') {
		if (system === 'metric') {
			return round(out, -2);
		} else {
			return round(out, -1);
		}
	} else if (type === 'temperature') {
		return round(out, -2);
	} else if (type === 'distance') {
		return round(out, -3);
	} else if (type === 'pressure') {
		if (system === 'metric') {
			return round(out, -1);
		} else {
			return round(out, -4);
		}
	} else if (type === 'lowSpeed') {
		return round(out, -2);
	} else if (type === 'highSpeed') {
		return round(out, -1);
	}
	return out;
}

export default Ember.Handlebars.makeBoundHelper(unitsValue);
