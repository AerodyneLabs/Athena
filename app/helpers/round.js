/**
 * Round a number to the specified precision
 * @method roundNumber
 * @param value {Number} The number to round
 * @param digits {Number} A number representing the desired precision
 * @return {Number} Rounded number
 */
export default function roundNumber(value, digits) {
	var val = Number(value);
	var dig = Number(digits);
	return Number(Math.round(val + 'e' + (-dig)) + ('e' + dig));
}
