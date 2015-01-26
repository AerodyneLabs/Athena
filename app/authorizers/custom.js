import Ember from 'ember';
import Base from 'simple-auth/authorizers/base';

export default Base.extend({
  authorize: function(jqXHR, requestOptions) {
    if(this.get('session.isAuthenticated') && !Ember.isEmpty(this.get('session.access_token'))) {
      jqXHR.setRequestHeader('Authorization', 'Token: ' + this.get('session.access_token'));
    }
  }
});
