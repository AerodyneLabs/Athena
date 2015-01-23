import Ember from 'ember';
import round from 'athena/helpers/round';

/**
 * Round a number to the specified precision
 * @method roundNumber
 * @param value {Number} The number to round
 * @param digits {Number} A number representing the desired precision
 * @return {Number} Rounded number
 */
export function roundNumber(value, digits) {
	return round(value, digits);
}

export default Ember.Handlebars.makeBoundHelper(roundNumber);
