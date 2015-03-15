var request = require('request');

exports = module.exports = function(app) {

  var mapquestApiKey = process.env.MAPQUEST_API_KEY;

  // Get a point from an address
  app.get('api/geo/address', function(req, res, next) {
    var baseUrl = 'http://open.mapquestapi.com/geocoding/v1/address';
    var url = baseUrl + '?key=' + mapquestApiKey;
    request.post({
      uri: url,
      json: true,
      body: {
        location: req.query.address,
        options: {
          maxResults: 1,
          thumbMaps: false
        }
      }
    }, function(error, response, body) {
      if(error) return next(error);

      var loc = body.results[0].locations[0];
      res.send({'location': {
        'type': 'Point',
        'coordinates': [loc.latLng.lng, loc.latLng.lat]
      }});
      return next();
    });
  });

  // Get an address from a point
  app.get('api/geo/reverse', function(req, res, next) {
    var baseUrl = 'http://open.mapquestapi.com/geocoding/v1/reverse';
    var url = baseUrl + '?key=' + mapquestApiKey;
    var coords = JSON.parse(req.query.location);
    request.post({
      uri: url,
      json: true,
      body: {
        location: {
          latLng: {
            lat: coords[1],
            lng: coords[0]
          }
        },
        options: {
          maxResults: 1,
          thumbMaps: false
        }
      }
    }, function(error, response, body) {
      if(error) return next(error);

      var address = body.results[0].locations[0];
      res.send({'address': {
        city: address.adminArea5,
        county: address.adminArea4,
        state: address.adminArea3,
        country: address.adminArea1,
        postalCode: address.postalCode
      }});
      return next();
    });
  });

  // Get ground level altitude
  app.get('api/geo/altitude', function(req, res, next) {
    var baseUrl = 'http://open.mapquestapi.com/elevation/v1/profile';
    var url = baseUrl + '?key=' + mapquestApiKey;
    var coords = JSON.parse(req.query.location);
    var latlngs = [];
    coords.forEach(function(x) {
      latlngs.push(x[1]);
      latlngs.push(x[0]);
    });
    request.post({
      uri: url,
      json: true,
      body: {
        latLngCollection: latlngs
      }
    }, function(error, response, body) {
      if(error) return next(error);

      var alts = body.elevationProfile;
      var result = new Array(coords.length);
      for(var i = 0; i < alts.length; i++) {
        result[i] = {
          type: 'Point',
          coordinates: [coords[i][0], coords[i][1], alts[i].height]
        };
      }
      res.send({'locations': result});
      return next();
    });
  });

};
