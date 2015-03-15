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
var atmosphere = require('./endpoints/atmosphere');
var geocoding = require('./endpoints/geocoding');
var prediction = require('./endpoints/prediction');

// Get environment variables
var googleClientId = process.env.GOOGLE_CLIENT_ID;

var server = restify.createServer();
server.use(restify.queryParser());
server.use(restify.bodyParser());

server.monk = monk;

var io = socketio.listen(server);

airspace(server);
atmosphere(server);
geocoding(server);
prediction(server);

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


// Start the server
server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
