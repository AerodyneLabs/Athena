import DS from 'ember-data';

export default DS.Model.extend({
	forecast: DS.attr('date'),
	analysis: DS.attr('date'),
	loc: DS.attr('point'),
	profile: DS.attr('array')	 
});
