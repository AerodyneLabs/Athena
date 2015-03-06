import Ember from 'ember';
import {configurable} from 'torii/configuration';
import Oauth2Bearer from 'torii/providers/oauth2-bearer';

var GoogleToken = Oauth2Bearer.extend({
  name: 'google-token',
  baseUrl: 'https://accounts.google.com/o/oauth2/auth',

  // additional params that this provider requires
  requiredUrlParams: ['state'],
  optionalUrlParams: ['scope', 'request_visible_actions', 'access_type'],

  requestVisibleActions: configurable('requestVisibleActions', ''),

  accessType: configurable('accessType', ''),

  responseParams: ['token'],

  scope: configurable('scope', 'email'),

  state: configurable('state', 'STATE'),

  redirectUri: configurable('redirectUri',
  'http://localhost:8000/oauth2callback'),

  open: function(){
    var name        = this.get('name'),
    url         = this.buildUrl(),
    redirectUri = this.get('redirectUri'),
    responseParams = this.get('responseParams');

    return this.get('popup').open(url, responseParams).then(function(authData){
      var missingResponseParams = [];

      responseParams.forEach(function(param){
        if (authData[param] === undefined) {
          missingResponseParams.push(param);
        }
      });

      if (missingResponseParams.length){
        throw "The response from the provider is missing " +
        "these required response params: " + responseParams.join(', ');
      }

      return Ember.$.get('api/validate', {access_token: authData.token}).then(function(data) {
        return {
          access_token: data.access_token,
          userEmail: data.email,
          expires: data.expires,
          provider: name,
          redirectUri: redirectUri
        };
      });
    });
  }
});

export default GoogleToken;
