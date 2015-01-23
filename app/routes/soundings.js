import Ember from 'ember';

/**
 * A route to display a list of all soundings
 * @class SoundingsRoute
 * @extends Ember.Route
 */
export default Ember.Route.extend({
	/**
	 * Set the model for the soundings route
	 * @method model
	 * @return {Promise} A promise that will resolve to an array of sounding models
	 */
	model: function() {
		return this.store.find('sounding');
	}
});
