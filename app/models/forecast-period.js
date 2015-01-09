import DS from 'ember-data';

export default DS.Model.extend({
	analysis: DS.attr('date'),
	forecast: DS.attr('date')
});
