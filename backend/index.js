// Require libraries
var restify = require('restify');
var celery = require('node-celery');

// Require endpoints
var airspace = require('./endpoints/airspace');
var atmosphere = require('./endpoints/atmosphere');
var geocoding = require('./endpoints/geocoding');
var prediction = require('./endpoints/prediction');
var user = require('./endpoints/user');

// Create server
var server = restify.createServer();
server.use(restify.queryParser());
server.use(restify.bodyParser());
server.celery = celery.createClient({
	CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672',
	CELERY_RESULT_BACKEND: 'amqp',
	CELERY_TASK_RESULT_EXPIRES: 3600
});;

// Initialize endpoints
airspace(server);
atmosphere(server);
geocoding(server);
prediction(server);
user(server);

// Start the server
server.listen(8080, function() {
	console.log('%s listening at %s', server.name, server.url);
});
