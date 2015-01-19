import Ember from 'ember';
import convert from 'athena/helpers/units';

export default Ember.Component.extend({
	tagName: 'svg',
	attributeBindings: 'width height'.w(),

	margin: {top: 20, right: 70, bottom: 30, left: 70},

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
		var presUnit = convert(units, 'pressure', 0).unit;
		var svg = d3.select('#'+this.get('elementId'));

		var tempScale = d3.scale.linear()
			.range([0, width])
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

		var line = d3.svg.line()
			.x(function(d) {
				return tempScale(convert(units, 'temperature', d['t']).value);
			})
			.y(function(d) {
				return altScale(convert(units, 'altitude', d['h']).value);
			})
			.interpolate('monotone');

		svg.select('.data').attr('d', line(data));
		svg.select('.axis.temperature')
			.call(tempAxis)
			.select('text')
			.attr('x', '0.5em')
			.attr('dy', '-.5em')
			.attr('text-anchor', 'start')
			.text('Temperature (' + tempUnit + ')');
		svg.select('.axis.altitude')
			.attr('transform', 'translate(' + width + ',0)')
			.call(altAxis)
			.select('text')
			.attr('transform', 'rotate(-90)')
			.attr('dy', '-.5em')
			.style('text-anchor', 'end')
			.text('Altitude (' + altUnit + ')');
		svg.select('.axis.pressure')
			.call(presAxis)
			.select('text')
			.attr('transform', 'rotate(-90)')
			.attr('dy', '1em')
			.style('text-anchor', 'end')
			.text('Pressure (' + presUnit + ')');
	}.observes('units'),

	didInsertElement: function() {
		this.draw();
	}
});
