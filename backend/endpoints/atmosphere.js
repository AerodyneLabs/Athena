exports = module.exports = function(app) {

  var atmosphere = app.monk('localhost/atmosphere');

  // Get many forecastPeriod records
  app.get('api/forecastPeriods', function(req, res, next) {
    var store = atmosphere.get('fs.files');
    store.find({}, '-chunkSize -md5', function(err, docs) {
      if(err) return next(err);

      res.send({'forecastPeriods':docs});
      return next();
    });
  });

  // Get specified forecastPeriod record
  app.get('api/forecastPeriods/:id', function(req, res, next) {
    var store = atmosphere.get('fs.files');
    store.findById(req.params.id, '-chunkSize -md5', function(err, doc) {
      if(err) return next(err);

      res.send({'forecastPeriod':doc});
      return next();
    });
  });

  // Get many sounding records
  app.get('api/soundings', function(req, res, next) {
    var store = atmosphere.get('forecast');
    var limit = req.query.limit || 25;
    var skip = req.query.offset || 0;
    var query = {};

    var total = 0;
    store.count(query, function(err, count) {
      if(err) return next(err);
      total = count;
    });
    store.find({}, {limit: limit, skip: skip}, function(err, docs) {
      if(err) return next(err);

      res.send({
        'soundings': docs,
        'meta': {
          'total': total,
          'offset': skip,
          'limit': limit
        }
      });
      return next();
    });
  });

  // Get specified sounding record
  app.get('api/soundings/:id', function(req, res, next) {
    var store = atmosphere.get('forecast');
    store.findById(req.params.id, function(err, doc) {
      if(err) return next(err);

      res.send({'sounding':doc});
      return next();
    });
  });

  // Extract soundings from compressed files
  var fetch_sounding = function(time, lat, lon, next) {
    var store = atmosphere.get('forecast');
    store.findOne({
      'forecast': time,
      'loc.coordinates': [lon, lat]
    }, function(err, doc) {
      if(doc) {
        if(next) {
          next(null, doc);
        }
        return;
      } else {
        var result = celery.call(
          'tasks.atmosphere.extract_sounding.extract_block',
          [time, lat, lon, 3]
        );
        result.once('success', function(data) {
          if(next) {
            store.findById(data.result[0], function(err, doc) {
              next(err, doc);
            });
          }
          return;
        });
        result.once('failed', function(data) {
          if(next) {
            next(data);
          }
          return;
        });
      }
    });
  };

  // Prefetch all soundings near a point
  app.post('api/soundings/prefetch', function(req, res, next) {
    var store = atmosphere.get('fs.files');
    if(req.params.near) {
      try {
        var coords = JSON.parse(req.params.near);
      } catch(SyntaxError) {
        return next(new restify.BadRequestError('"near" parameter invalid!'));
      }
      var lat = Number(coords[1]);
      var lon = Number(coords[0]);
      if(
        isNaN(lat) || isNaN(lon) ||
        lat <= -90 || lat >= 90 ||
        lon <= -180 || lon > 180
      ) {
        return next(new restify.BadRequestError('"near" parameter invalid!'));
      }
      var now = new Date();
      var filter = new Date(now.getTime() - (6 * 60 * 60 * 1000));
      console.log('Filtering > ', filter);
      store.find({
        forecast: {
          $gte: filter
        }
      }, 'forecast', function(err, docs) {
        if(err) return next(err);

        for(var i = 0; i < docs.length; i++) {
          fetch_sounding(docs[i].forecast, lat, lon);
        }

        res.send({fetching: docs});
        return next();
      });
    } else {
      return next(new restify.BadRequestError('"near" query parameter missing!'));
    }
  });

  // Get sounding from database
  app.get('api/sounding/:timestamp/:latitude/:longitude', function(req, res, next) {
    var time = new Date(Number(req.params.timestamp) * 1000);
    var lat = Number(req.params.latitude);
    var lon = Number(req.params.longitude);
    var store = atmosphere.get('forecast');
    store.findOne({
      'forecast': time,
      'loc.coordinates':[lon, lat]
    }, function(err, docs) {
      if(docs) {
        res.send({sounding:docs});
        next();
      } else {
        var result = celery.call(
          'atmosphereTasks.extract_forecast',
          [time, lat, lon]
        );
        result.once('success', function(data) {
          store.findById(data.result[0], function(err, doc) {
            res.send({sounding:doc});
          });
        });
        result.once('failed', function(data) {
          res.send(data);
        });
      }
    });
  });

};
