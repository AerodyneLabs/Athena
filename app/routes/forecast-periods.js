import Ember from 'ember';

/**
 * A route to display a list of all forecast periods
 * @class ForecastPeriodsRoute
 * @extends Ember.Route
 */
export default Ember.Route.extend({
	/**
	 * Set the model for the forecast periods route
	 * @method model
	 * @return {Promise} A promise that will resolve to an array of forecast period models
	 */
	model: function() {
		return this.store.find('forecastPeriod');
	}
});
