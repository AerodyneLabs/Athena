var restify = require('restify');

function version(req, res, next) {
	res.send({
		version: '0.0.1'
	});
	next();
}

var server = restify.createServer();

server.get('api/version', version);

server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
