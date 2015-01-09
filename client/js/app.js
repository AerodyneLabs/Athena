App = Ember.Application.create();

App.ApplicationAdapter = DS.RESTAdapter.extend({
	namespace: 'api'
});

App.Router.map(function() {
	this.route('about');

	this.resource('forecastPeriods');
	//this.resource('sounding', {path: '/sounding/:sounding_id'});
});

App.ForecastPeriodsRoute = Ember.Route.extend({
	model: function() {
		return this.store.find('forecastPeriod');
	}
});

App.ForecastPeriod = DS.Model.extend({
	analysis: DS.attr('date'),
	forecast: DS.attr('date')
});

App.ApplicationSerializer = DS.RESTSerializer.extend({
	primaryKey: '_id'
});
