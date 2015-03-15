exports = module.exports = function(app) {

  var airspace = app.monk('localhost/airspace');

  // Get many center records
  app.get('api/centers', function(req, res, next) {
    var store = airspace.get('artcc');
    var query = {};
    if(req.query.near) {
      var coords = JSON.parse(req.query.near);
      query = {
        geometry: {
          $geoIntersects: {
            $geometry: {
              type: 'Point',
              coordinates: coords
            }
          }
        }
      };
    }
    if(req.query.within) {
      var coords = JSON.parse(req.query.within);
      var box = [
      coords[0],
      [coords[1][0], coords[0][1]],
      coords[1],
      [coords[0][0], coords[1][1]],
      coords[0]
      ];
      query = {
        geometry: {
          $geoIntersects: {
            $geometry: {
              type: 'Polygon',
              coordinates: [box]
            }
          }
        }
      };
    }
    store.find(query, function(err, docs) {
      if(err) return next(err);

      res.send({'centers': docs});
      return next();
    });
  });

  // Get a specified center record
  app.get('api/centers/:id', function(req, res, next) {
    var store = airspace.get('artcc');
    store.id = function(str) {return str;};
    store.findById(req.params.id, function(err, doc) {
      if(err) return next(err);

      res.send({'center': doc});
      return next();
    });
  });

  // Get many navaid records
  app.get('api/navaids', function(req, res, next) {
    var store = airspace.get('navaid');
    var limit = req.query.limit || 25;
    var skip = req.query.offset || 0;
    var query = {};
    if(req.query.near) {
      var coords = JSON.parse(req.query.near);
      query = {
        geometry: {
          $near: {
            $geometry: {
              type: 'Point',
              coordinates: coords
            }
          }
        }
      };
    }
    if(req.query.within) {
      var coords = JSON.parse(req.query.within);
      query = {
        geometry: {
          $geoWithin: {
            $box: coords
          }
        }
      };
    }
    var total = 0;
    store.count(query, function(err, count) {
      if(err) return next(err);
      total = count;
    });
    store.find(query, {limit: limit, skip: skip}, function(err, docs) {
      if(err) return next(err);

      res.send({
        'navaids': docs,
        'meta': {
          'total': total,
          'offset': skip,
          'limit': limit
        }
      });
      return next();
    });
  });

  // Get specified navaid record
  app.get('api/navaids/:id', function(req, res, next) {
    var store = airspace.get('navaid');
    store.id = function(str) {return str;};
    store.findById(req.params.id, function(err, doc) {
      if(err) return next(err);

      res.send({'navaid': doc});
      return next();
    });
  });

  // Get many tower records
  app.get('api/towers', function(req, res, next) {
    var store = airspace.get('tower');
    var limit = req.query.limit || 25;
    var skip = req.query.offset || 0;
    var query = {};
    if(req.query.near) {
      var coords = JSON.parse(req.query.near);
      query = {
        geometry: {
          $near: {
            $geometry: {
              type: 'Point',
              coordinates: coords
            }
          }
        }
      };
    }
    if(req.query.within) {
      var coords = JSON.parse(req.query.within);
      query = {
        geometry: {
          $geoWithin: {
            $box: coords
          }
        }
      };
    }
    var total = 0;
    store.count(query, function(err, count) {
      if(err) return next(err);
      total = count;
    });
    store.find(query, {limit: limit, skip: skip}, function(err, docs) {
      if(err) return next(err);

      res.send({
        'towers': docs,
        'meta': {
          'total': total,
          'offset': skip,
          'limit': limit
        }
      });
      return next();
    });
  });

  // Get a specified tower record
  app.get('api/towers/:id', function(req, res, next) {
    var store = airspace.get('tower');
    store.id = function(str) {return str;};
    store.findById(req.params.id, function(err, doc) {
      if(err) return next(err);

      res.send({'tower': doc});
      return next();
    });
  });

};
