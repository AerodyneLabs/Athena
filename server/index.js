var restify = require('restify');
var socketio = require('socket.io');
var monk = require('monk')('localhost/atmosphere');
var celery = require('node-celery').createClient({
	CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672',
	CELERY_RESULT_BACKEND: 'amqp',
	CELERY_TASK_RESULT_EXPIRES: 3600
});

function version(req, res, next) {
	res.send({
		version: '0.0.1'
	});
	next();
}

var server = restify.createServer();
var io = socketio.listen(server);

server.get('api/version', version);

// Get sounding from database
server.get('api/sounding/:timestamp/:latitude/:longitude', function(req, res, next) {
	var time = new Date(Number(req.params.timestamp));
	var lat = Number(req.params.latitude);
	var lon = Number(req.params.longitude);
	var store = monk.get('forecast');
	store.findOne({
		'forecast': time,
		'loc.coordinates':[lon, lat]
	}, function(err, docs) {
		if(docs) {
			res.send(docs);
			return;
		} else {
			var result = celery.call(
				'datastoreTasks.extract_forecast',
				[time, lat, lon]
			);
			result.once('success', function(data) {
				store.findById(data.result[0], function(err, doc) {
					res.send(doc);
				});
			});
			result.once('failed', function(data) {
				res.send(data);
			});
		}
	});
});

server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
