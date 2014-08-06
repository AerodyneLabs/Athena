var restify = require('restify');
var socketio = require('socket.io');
var monk = require('monk')('localhost/atmosphere');

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
	store.find({
		'forecast': time,
		'loc.coordinates':[lon, lat]
	}, function(err, docs) {
		res.send(docs);
	});
});

server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
