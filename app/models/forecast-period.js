import DS from 'ember-data';

/**
 * Model of a single atmospheric forecast period
 * @class ForecastPeriodModel
 * @extends DS.Model
 */
export default DS.Model.extend({
	/**
	 * Date and time the forecast period was analyzed
	 * @property analysis
	 * @type Date
	 */
	analysis: DS.attr('date'),

	/**
	 * Date and time the forecast period represents
	 * @property forecast
	 * @type Date
	 */
	forecast: DS.attr('date'),

	/**
	 * Size of the forecast period file in bytes
	 * @property length
	 * @type Number
	 */
	length: DS.attr('number'),

	/**
	 * Date and time the forecast period was uploaded
	 * @property uploadDate
	 * @type Date
	 */
	uploadDate: DS.attr('date'),
});
