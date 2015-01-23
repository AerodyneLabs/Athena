import Ember from 'ember';

/**
 * A route to display a single sounding
 * @class SoundingRoute
 * @extends Ember.Route
 */
export default Ember.Route.extend({
	/**
	 * Set the model for the sounding route to be the given sounding id
	 * @method model
	 * @param params {Object} params.id contains the id of the target sounding
	 * @return {Promise} A promise that will resolve to a sounding model
	 */
	model: function(params) {
		return this.store.find('sounding', params.id);
	}
});
