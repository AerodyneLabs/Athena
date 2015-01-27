import Ember from 'ember';
import LoginControllerMixin from 'simple-auth/mixins/login-controller-mixin';

/**
 * Application wide controller
 * @class ApplicationController
 * @extends Ember.Controller
 */
export default Ember.Controller.extend(LoginControllerMixin, {
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
	}],

	authenticator: 'authenticator:torii',
	actions: {
		loginWithGoogle: function() {
			var _this = this;
			this.get('session')
			.authenticate('simple-auth-authenticator:torii', 'google-token')
			.then(function() {
				console.log('Authorized: ', _this.get('session.userEmail'));
			}, function(error) {
				console.log('Error: ', error);
			});
		}
	}
});
