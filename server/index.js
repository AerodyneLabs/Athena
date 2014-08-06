var restify = require('restify');
var socketio = require('socket.io');
var mongo = require('mongodb');
var monk = require('monk');
var db = monk('localhost:27017/atmosphere');


function version(req, res, next) {
	res.send({
		version: '0.0.1'
	});
	next();
}

var server = restify.createServer();
var io = socketio.listen(server);

server.use(function(req, res, next) {
	req.db = db;
	next();
});

server.get('api/version', version);

// Get sounding from database
server.get('api/sounding/:timestamp/:latitude/:longitude', function(req, res, next) {
});

server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
