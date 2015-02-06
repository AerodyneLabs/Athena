var restify = require('restify');
var socketio = require('socket.io');
var monk = require('monk')('localhost/atmosphere');
var airspace = require('monk')('localhost/airspace');
var celery = require('node-celery').createClient({
	CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672',
	CELERY_RESULT_BACKEND: 'amqp',
	CELERY_TASK_RESULT_EXPIRES: 3600
});

var server = restify.createServer();
server.use(restify.queryParser());

var io = socketio.listen(server);

server.get('api/version', function version(req, res, next) {
	res.send({
		version: '0.0.1'
	});
	return next();
});

server.get('api/forecastPeriods', function(req, res, next) {
	var store = monk.get('fs.files');
	store.find({}, '-chunkSize -md5', function(err, docs) {
		if(err) return next(err);

		res.send({'forecastPeriods':docs});
		return next();
	});
});

server.get('api/forecastPeriods/:id', function(req, res, next) {
	var store = monk.get('fs.files');
	store.findById(req.params.id, '-chunkSize -md5', function(err, doc) {
		if(err) return next(err);

		res.send({'forecastPeriod':doc});
		return next();
	});
});

server.get('api/towers', function(req, res, next) {
	var store = airspace.get('tower');
	var limit = req.query.limit || 25;
	var skip = req.query.skip || 0;
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
	store.find(query, {limit: limit, skip: skip}, function(err, docs) {
		if(err) return next(err);

		res.send({'towers': docs});
		return next();
	});
});

server.get('api/towers/:id', function(req, res, next) {
	var store = airspace.get('tower');
	store.id = function(str) {return str;};
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'center': doc});
		return next();
	});
});

server.get('api/centers', function(req, res, next) {
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

server.get('api/centers/:id', function(req, res, next) {
	var store = airspace.get('artcc');
	store.id = function(str) {return str;};
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'center': doc});
		return next();
	});
});

server.get('api/soundings', function(req, res, next) {
	var store = monk.get('forecast');
	store.find({}, function(err, docs) {
		if(err) return next(err);

		res.send({'soundings':docs});
		return next();
	});
});

server.get('api/soundings/:id', function(req, res, next) {
	var store = monk.get('forecast');
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'sounding':doc});
		return next();
	});
});

// Get sounding from database
server.get('api/sounding/:timestamp/:latitude/:longitude', function(req, res, next) {
	var time = new Date(Number(req.params.timestamp) * 1000);
	var lat = Number(req.params.latitude);
	var lon = Number(req.params.longitude);
	var store = monk.get('forecast');
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

server.get('api/navaids', function(req, res, next) {
	var store = airspace.get('navaid');
	var limit = req.query.limit || 25;
	var skip = req.query.skip || 0;
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
	store.find(query, {limit: limit, skip: skip}, function(err, docs) {
		if(err) return next(err);

		res.send({'navaids': docs});
		return next();
	});
});

server.get('api/navaids/:id', function(req, res, next) {
	var store = airspace.get('navaid');
	store.id = function(str) {return str;};
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'navaid': doc});
		return next();
	});
});

server.get('api/airspaces/:lat1/:lon1/:lat2/:lon2', function(req, res, next) {
	var lat1 = Number(req.params.lat1);
	var lon1 = Number(req.params.lon1);
	var lat2 = Number(req.params.lat2);
	var lon2 = Number(req.params.lon2);
	var store = airspace.get('airspaces');
	store.find({
		'bounds': {
			'$geoIntersects': {
				'$geometry': {
					'type': 'Polygon',
					'coordinates': [[
						[lon1, lat1],
						[lon2, lat1],
						[lon2, lat2],
						[lon1, lat2],
						[lon1, lat1]
					]]
				}
			}
		}
	}, function(err, docs) {
		if(err) {
			res.send(400, err);
		} else {
			var features = {
				'type': 'FeatureCollection',
				'features': docs
			}
			res.send(features);
		}
	});
});

server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
