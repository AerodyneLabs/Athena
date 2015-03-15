var monk = require('monk');

exports = module.exports = function(app) {

  var flights = monk('localhost/flights');

  // Get many prediction records
  app.get('api/predictions', function(req, res, next) {
    var store = flights.get('predictions');
    store.find({}, function(err, docs) {
      if(err) return next(err);

      res.send({'predictions': docs});
      return next();
    });
  });

  // Get specified prediction record
  app.get('api/predictions/:id', function(req, res, next) {
    var store = flights.get('predictions');
    store.findById(req.params.id, function(err, doc) {
      if(err) return next(err);

      res.send({'prediction': doc});
      return next();
    });
  });

  // Create a new prediction
  app.post('api/predictions', function(req, res, next) {
    var store = flights.get('predictions');
    var params = req.params.prediction;
    var result = app.celery.call(
      'tasks.predictor.latex1v0.run_prediction',
      [params]
    );
    result.once('success', function(data) {
      store.insert(data.result, function(err, doc) {
        if(err) return next(err);

        res.send({'prediction': doc});
        return next();
      });
    });
    result.once('failed', function(data) {
      return next(data);
    });
  });

  // Get many flight records
  app.get('api/flights', function(req, res, next) {
    var store = flights.get('flights');
    var query = {};
    if(req.query.status) {
      if(req.query.status == 'current') {
        query.status = 'current';
      } else if(req.query.status == 'upcoming') {
        query.launchTime = {
          $gt: new Date()
        }
      }
    }
    store.find(query, function(err, docs) {
      if(err) return next(err);

      res.send({'flights': docs});
      return next();
    });
  });

  // Get specified flight record
  app.get('api/flights/:id', function(req, res, next) {
    var store = flights.get('flights');
    store.findById(req.params.id, function(err, doc) {
      if(err) return next(err);

      res.send({'flight': doc});
      return next();
    });
  });

};
