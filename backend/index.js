var restify = require('restify');
var socketio = require('socket.io');
var monk = require('monk');
var request = require('request');
var celery = require('node-celery').createClient({
	CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672',
	CELERY_RESULT_BACKEND: 'amqp',
	CELERY_TASK_RESULT_EXPIRES: 3600
});

var airspace = require('./endpoints/airspace');
var geocoding = require('./endpoints/geocoding');

// Get environment variables
var googleClientId = process.env.GOOGLE_CLIENT_ID;

// Get database collections
var atmosphere = monk('localhost/atmosphere');
var flights = monk('localhost/flights');

var server = restify.createServer();
server.use(restify.queryParser());
server.use(restify.bodyParser());

server.monk = monk;

var io = socketio.listen(server);

airspace(server);
geocoding(server);

// Misc routes

// Get the server version
server.get('api/version', function version(req, res, next) {
	res.send({
		version: '0.0.1'
	});
	return next();
});

// Validate an access token
server.get('api/validate', function(req, res, next) {
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

// Prediction/flight routes

// Get many prediction records
server.get('api/predictions', function(req, res, next) {
	var store = flights.get('predictions');
	store.find({}, function(err, docs) {
		if(err) return next(err);

		res.send({'predictions': docs});
		return next();
	});
});

// Get specified prediction record
server.get('api/predictions/:id', function(req, res, next) {
	var store = flights.get('predictions');
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'prediction': doc});
		return next();
	});
});

// Create a new prediction
server.post('api/predictions', function(req, res, next) {
	var store = flights.get('predictions');
	var params = req.params.prediction;
	var result = celery.call(
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
server.get('api/flights', function(req, res, next) {
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
server.get('api/flights/:id', function(req, res, next) {
	var store = flights.get('flights');
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'flight': doc});
		return next();
	});
});


// Atmosphere routes

// Get many forecastPeriod records
server.get('api/forecastPeriods', function(req, res, next) {
	var store = atmosphere.get('fs.files');
	store.find({}, '-chunkSize -md5', function(err, docs) {
		if(err) return next(err);

		res.send({'forecastPeriods':docs});
		return next();
	});
});

// Get specified forecastPeriod record
server.get('api/forecastPeriods/:id', function(req, res, next) {
	var store = atmosphere.get('fs.files');
	store.findById(req.params.id, '-chunkSize -md5', function(err, doc) {
		if(err) return next(err);

		res.send({'forecastPeriod':doc});
		return next();
	});
});

// Get many sounding records
server.get('api/soundings', function(req, res, next) {
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
server.get('api/soundings/:id', function(req, res, next) {
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
server.post('api/soundings/prefetch', function(req, res, next) {
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
server.get('api/sounding/:timestamp/:latitude/:longitude', function(req, res, next) {
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


// Start the server
server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
