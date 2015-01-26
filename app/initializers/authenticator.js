import Ember from 'ember';
import AuthenticatorTorii from 'simple-auth-torii/authenticators/torii';

export function initialize(/* container, application */) {
  AuthenticatorTorii.reopen({
    restore: function(data) {
      var resolveData = data || {};
      this.provider = resolveData.provider;
      return new Ember.RSVP.Promise(function(resolve) {
        resolve(resolveData || {});
      });
    }
  });
}

export default {
  name: 'authenticator',
  before: 'simple-auth-torii',
  initialize: initialize
};
