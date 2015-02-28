import Ember from 'ember';
import LoginControllerMixin from 'simple-auth/mixins/login-controller-mixin';

/**
 * Application wide controller
 * @class ApplicationController
 * @extends Ember.Controller
 */
export default Ember.Controller.extend(LoginControllerMixin, {
	units: {
		altitude: 'm',
		distance: 'km',
		length: 'cm',
		mass: 'kg',
		pressure: 'Pa',
		speed: 'm/s',
		temperature: 'C'
	},

	unitOptions: {
		altitude: ['m', 'km', 'ft', 'mi'],
		distance: ['km', 'mi', 'nm'],
		length: ['cm', 'm', 'in', 'ft'],
		mass: ['kg', 'lb'],
		pressure: ['Pa', 'hPa', 'Psi', 'mmHg', 'inMg'],
		speed: ['m/s', 'kph', 'f/s', 'mph', 'kts'],
		temperature: ['C', 'F']
	},

	time: new Date(),

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
