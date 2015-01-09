App = Ember.Application.create();

App.ApplicationAdapter = DS.RESTAdapter.extend({
	namespace: 'api'
});

App.Router.map(function() {
	this.route('about');

	this.resource('soundings');
	//this.resource('sounding', {path: '/sounding/:sounding_id'});
});

App.SoundingsRoute = Ember.Route.extend({
	model: function() {
		return this.store.find('sounding');
	}
});

App.Sounding = DS.Model.extend({
	analysis: DS.attr('date'),
	forecast: DS.attr('date')
});

App.ApplicationSerializer = DS.RESTSerializer.extend({
	primaryKey: '_id'
});
