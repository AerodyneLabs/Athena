import Ember from 'ember';
import convert from 'athena/helpers/units';

export default Ember.Component.extend({
	tagName: 'svg',
	attributeBindings: 'width height'.w(),

	margin: {top: 20, right: 70, bottom: 30, left: 70},
	padding: 20,

	w: function() {
		return this.get('width') - this.get('margin.left') - this.get('margin.right');
	}.property('width'),

	h: function() {
		return this.get('height') - this.get('margin.top') - this.get('margin.bottom');
	}.property('height'),

	tempWidth: function() {
		return Math.round(0.7 * (this.get('w') - this.get('padding')));
	}.property('width'),

	windWidth: function() {
		return this.get('w') - this.get('tempWidth') - this.get('padding');
	}.property('tempWidth'),

	transformG: function() {
		return "translate(" + this.get('margin.left') + "," + this.get('margin.top') + ")";
	}.property(),

	transformX: function() {
		return "translate(0,"+ this.get('h') +")";
	}.property('h'),

	transformWind: function() {
		return "translate(" + (this.get('tempWidth') + this.get('padding')) + "," + this.get('h') + ")";
	}.property('h'),

	transformAlt: function() {
		return "translate(" + this.get('w') + ",0)";
	}.property('width'),

	draw: function() {
		var height = this.get('h');
		var data = this.get('data');
		var units = this.get('units');
		var tempWidth = this.get('tempWidth');
		var windWidth = this.get('windWidth');
		var padding = this.get('padding');
		var svg = d3.select('#'+this.get('elementId'));

		var tempScale = d3.scale.linear()
			.range([0, tempWidth])
			.domain(d3.extent(data, function(d) {
				return convert(units, 'temperature', d['t']).value;
			}));
		var altScale = d3.scale.linear()
			.range([height, 0])
			.domain(d3.extent(data, function(d) {
				return convert(units, 'altitude', d['h']).value;
			}));
		var presScale = d3.scale.log()
			.range([0, height])
			.domain(d3.extent(data, function(d) {
				return convert(units, 'pressure', d['p']).value;
			}));
		var windScale = d3.scale.linear()
			.range([0, windWidth])
			.domain([0, d3.max(data, function(d) {
				return convert(units, 'highSpeed', d['ws']).value;
			})]);

		var tempAxis = d3.svg.axis()
			.scale(tempScale)
			.orient('bottom');
		var altAxis = d3.svg.axis()
			.scale(altScale)
			.orient('right');
		var presAxis = d3.svg.axis()
			.scale(presScale)
			.orient('left')
			.tickFormat(d3.format('d'));
		var windAxis = d3.svg.axis()
			.scale(windScale)
			.orient('bottom')
			.ticks(4);

		var line = d3.svg.line()
			.x(function(d) {
				return tempScale(convert(units, 'temperature', d['t']).value);
			})
			.y(function(d) {
				return altScale(convert(units, 'altitude', d['h']).value);
			})
			.interpolate('linear');

		var wind = d3.svg.line()
			.x(function(d) {
				return windScale(convert(units, 'highSpeed', d['ws']).value) + tempWidth + padding;
			})
			.y(function(d) {
				return altScale(convert(units, 'altitude', d['h']).value);
			})
			.interpolate('linear');

		svg.select('.data.temperature').attr('d', line(data));
		svg.select('.data.wind').attr('d', wind(data));
		svg.select('.axis.temperature')
			.call(tempAxis);
		svg.select('.axis.altitude')
			.call(altAxis);
		svg.select('.axis.pressure')
			.call(presAxis);
		svg.select('.axis.wind')
			.call(windAxis);
	}.observes('units'),

	didInsertElement: function() {
		this.draw();
	}
});
