var request = require('request');

exports = module.exports = function(app) {

  var googleClientId = process.env.GOOGLE_CLIENT_ID;

  // Validate an access token
  app.get('api/validate', function(req, res, next) {
    request.get({
      uri: 'https://www.googleapis.com/oauth2/v1/tokeninfo',
      qs: {
        access_token: req.params.access_token
      }
    }, function(error, response, body) {
      if(error) return next(error);

      var resp = JSON.parse(body);
      if(resp.audience === googleClientId) {
        res.send({
          access_token: req.params.access_token,
          email: resp.email,
          expires: resp.expires_in
        });
      } else {
        return next('Token invalid!');
      }
    });
  });

};
