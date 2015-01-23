import Ember from 'ember';

/**
 * A route to display a single forecast period
 * @class ForecastPeriodRoute
 * @extends Ember.Route
 */
export default Ember.Route.extend({
	/**
	 * Set the model for the forecast period route to be the given period id
	 * @method model
	 * @param params {Object} params.id contains the id of the target forecast period
	 * @return {Promise} A promise that will resolve to a forecast period model
	 */
	model: function(params) {
		return this.store.find('forecastPeriod', params.id);
	}
});
