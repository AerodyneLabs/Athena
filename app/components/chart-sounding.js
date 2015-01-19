import Ember from 'ember';
import convert from 'athena/helpers/units';

export default Ember.Component.extend({
	tagName: 'svg',
	attributeBindings: 'width height'.w(),

	margin: {top: 20, right: 20, bottom: 30, left: 70},

	w: function() {
		return this.get('width') - this.get('margin.left') - this.get('margin.right');
	}.property('width'),

	h: function() {
		return this.get('height') - this.get('margin.top') - this.get('margin.bottom');
	}.property('height'),

	transformG: function() {
		return "translate(" + this.get('margin.left') + "," + this.get('margin.top') + ")";
	}.property(),

	transformX: function() {
		return "translate(0,"+ this.get('h') +")";
	}.property('h'),

	draw: function() {
		var width = this.get('w');
		var height = this.get('h');
		var data = this.get('data');
		var units = this.get('units');
		var altUnit = convert(units, 'altitude', 0).unit;
		var tempUnit = convert(units, 'temperature', 0).unit;
		var svg = d3.select('#'+this.get('elementId'));

		var xScale = d3.scale.linear().range([0, width]);
		xScale.domain(d3.extent(data, function(d) {
			return convert(units, 'temperature', d['t']).value;
		}));
		var yScale = d3.scale.linear().range([height, 0]);
		yScale.domain(d3.extent(data, function(d) {
			return convert(units, 'altitude', d['h']).value;
		}));

		var xAxis = d3.svg.axis().scale(xScale).orient('bottom');
		var yAxis = d3.svg.axis().scale(yScale).orient('left');

		var line = d3.svg.line()
			.x(function(d) {
				return xScale(convert(units, 'temperature', d['t']).value);
			})
			.y(function(d) {
				return yScale(convert(units, 'altitude', d['h']).value);
			})
			.interpolate('monotone');

		svg.select('.data').attr('d', line(data));
		svg.select('.axis.x')
			.call(xAxis)
			.select('text')
			.attr('x', width)
			.attr('dy', '-.5em')
			.attr('text-anchor', 'end')
			.text('Temperature (' + tempUnit + ')');
		svg.select('.axis.y')
			.call(yAxis)
			.select('text')
			.attr('transform', 'rotate(-90)')
			.attr('dy', '1em')
			.style('text-anchor', 'end')
			.text('Altitude (' + altUnit + ')');
	}.observes('units'),

	didInsertElement: function() {
		this.draw();
	}
});
