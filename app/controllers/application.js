import Ember from 'ember';

/**
 * Application wide controller
 * @class ApplicationController
 * @extends Ember.Controller
 */
export default Ember.Controller.extend({
	/**
	 * Default unit system id
	 * @property unts
	 * @type String
	 */
	units: 'metric',

	/**
	 * Array of unit systems
	 * @property unitsOptions
	 * @type Array
	 */
	unitsOptions: [{
		id: 'imperial',
		name: 'Imperial'
	}, {
		id: 'metric',
		name: 'Metric'
	}]
});
