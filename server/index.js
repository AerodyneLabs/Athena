var restify = require('restify');
var socketio = require('socket.io');

function version(req, res, next) {
	res.send({
		version: '0.0.1'
	});
	next();
}

var server = restify.createServer();
var io = socketio.listen(server);

server.get('api/version', version);

server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
