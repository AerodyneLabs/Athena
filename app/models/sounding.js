import DS from 'ember-data';

/**
 * Model of a single atmospheric sounding
 * @class SoundingModel
 * @extends DS.Model
 */
export default DS.Model.extend({
	/**
	 * Date and time the sounding represents
	 * @property forecast
	 * @type Date
	 */
	forecast: DS.attr('date'),

	/**
	 * Date and time the sounding was analyzed
	 * @property analysis
	 * @type Date
	 */
	analysis: DS.attr('date'),

	/**
	 * Geographic location the sounding represents
	 * @property loc
	 * @type Point
	 */
	loc: DS.attr('point'),

	/**
	 * Sounding data array
	 * @property profile
	 * @type Array
	 */
	profile: DS.attr('array')
});
