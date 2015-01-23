import Ember from 'ember';

/**
 * Sounding controller to decorate sounding models
 * @class SoundingController
 * @extends Ember.ObjectController
 */
export default Ember.ObjectController.extend({
	/**
	 * Controller dependencies
	 * @property needs
	 * @type {Array}
	 */
	needs: ['application'],

	/**
	 * Decorate sounding model with computed wind speed and direction
	 * @method profile
	 * @return {SoundingModel} Decorated model
	 */
	profile: function() {
		var model = this.get('model.profile');
		for (var i = 0; i < model.length; i++) {
			var obs = model[i];
			var u = obs.u;
			var v = obs.v;
			obs['ws'] = Math.sqrt(Math.pow(u, 2) + Math.pow(v, 2));
			var dir = Math.atan2(u, v) * 180.0 / Math.PI;
			if (dir < 0) {
				dir = dir + 360.0;
			}
			obs['wd'] = dir;
		}
		return model;
	}.property('model.profile')
});
