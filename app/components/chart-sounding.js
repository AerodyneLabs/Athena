import Ember from 'ember';

export default Ember.Component.extend({
	tagName: 'svg',
	attributeBindings: 'width height'.w(),

	margin: {top: 20, right: 20, bottom: 30, left: 100},

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
		var svg = d3.select('#'+this.get('elementId'));

		var xScale = d3.scale.linear().range([0, width]);
		xScale.domain(d3.extent(data, function(d) {
			return d['t'];
		}));
		var yScale = d3.scale.linear().range([height, 0]);
		yScale.domain(d3.extent(data, function(d) {
			return d['h'];
		}));

		var xAxis = d3.svg.axis().scale(xScale).orient('bottom');
		var yAxis = d3.svg.axis().scale(yScale).orient('left');

		var line = d3.svg.line()
			.x(function(d) {
				console.log('x ' + d['t'] + ' ' + xScale(d['t']));
				return xScale(d['t']);
			})
			.y(function(d) {
				console.log('y ' + d['h'] + ' ' + yScale(d['h']));
				return yScale(d['h']);
			})
			.interpolate('monotone');

		console.log(line(data));

		svg.select('.axis.x').call(xAxis);
		svg.select('.axis.y').call(yAxis);
		svg.select('.data').attr('d', line(data));
	},

	didInsertElement: function() {
		this.draw();
	}
});
