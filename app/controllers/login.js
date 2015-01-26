import Ember from 'ember';
import LoginControllerMixin from 'simple-auth/mixins/login-controller-mixin';

export default Ember.Controller.extend(LoginControllerMixin, {
  authenticator: 'authenticator:torii',
  actions: {
    loginWithGoogle: function() {
      var _this = this;
      this.get('session')
        .authenticate('simple-auth-authenticator:torii', 'google-oauth2')
        .then(function() {
          var authCode = _this.get('session.authorizationCode');
          console.log('Authorized: ', _this.get('session.content'));
          $.get('https://www.googleapis.com/plus/v1/people/me', {access_token: authCode})
            .then(function(user) {
              console.log(user);
            });
        }, function(error) {
          console.log('Error: ', error);
        });
    }
  }
});
