var restify = require('restify');
var socketio = require('socket.io');
var monk = require('monk')('localhost/atmosphere');
var airspace = require('monk')('localhost/airspace');
var flights = require('monk')('localhost/flights');
var request = require('request');
var celery = require('node-celery').createClient({
	CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672',
	CELERY_RESULT_BACKEND: 'amqp',
	CELERY_TASK_RESULT_EXPIRES: 3600
});

var server = restify.createServer();
server.use(restify.queryParser());
server.use(restify.bodyParser());

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

server.get('api/predictions', function(req, res, next) {
	var store = flights.get('predictions');
	store.find({}, function(err, docs) {
		if(err) return next(err);

		res.send({'predictions': docs});
		return next();
	});
});

server.get('api/predictions/:id', function(req, res, next) {
	var store = flights.get('predictions');
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'prediction': doc});
		return next();
	});
});

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

server.get('api/flights/:id', function(req, res, next) {
	var store = flights.get('flights');
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'flight': doc});
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

var fetch_sounding = function(time, lat, lon, next) {
	var store = monk.get('forecast');
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
				'tasks.atmosphere.extract_sounding.extract_sounding',
				[time, lat, lon]
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

server.get('api/soundings/:id', function(req, res, next) {
	var store = monk.get('forecast');
	store.findById(req.params.id, function(err, doc) {
		if(err) return next(err);

		res.send({'sounding':doc});
		return next();
	});
});

server.post('api/soundings/prefetch', function(req, res, next) {
	var store = monk.get('fs.files');
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

server.get('api/geo/address', function(req, res, next) {
	var baseUrl = 'http://open.mapquestapi.com/geocoding/v1/address';
	var url = baseUrl + '?key=' + process.env.MAPQUEST_API_KEY;
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

server.get('api/geo/reverse', function(req, res, next) {
	var baseUrl = 'http://open.mapquestapi.com/geocoding/v1/reverse';
	var url = baseUrl + '?key=' + process.env.MAPQUEST_API_KEY;
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

server.get('api/geo/altitude', function(req, res, next) {
	var baseUrl = 'http://open.mapquestapi.com/elevation/v1/profile';
	var url = baseUrl + '?key=' + process.env.MAPQUEST_API_KEY;
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
