import Ember from 'ember';
import LoginControllerMixin from 'simple-auth/mixins/login-controller-mixin';

/**
 * Application wide controller
 * @class ApplicationController
 * @extends Ember.Controller
 */
export default Ember.Controller.extend(LoginControllerMixin, {
	altitudeUnit: 'm',
	altitudeUnits: [
		'm',
		'km',
		'ft',
		'mi'
	],

	distanceUnit: 'km',
	distanceUnits: [
		'km',
		'mi',
		'nm'
	],

	massUnit: 'kg',
	massUnits: [
		'kg',
		'lb'
	],

	speedUnit: 'm/s',
	speedUnits: [
		'm/s',
		'kph',
		'f/s',
		'mph',
		'kts'
	],

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
