import Ember from 'ember';
import convert from 'athena/helpers/units';

export default Ember.Component.extend({
	tagName: 'svg',
	attributeBindings: 'width height'.w(),

	margin: {top: 10, right: 20, bottom: 40, left: 80},
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

	verticalLabel: function() {
		return -(this.get('h') / 2.0);
	}.property('h'),

	tempLabel: function() {
		return this.get('tempWidth') / 2.0;
	}.property('tempWidth'),

	windLabel: function() {
		return this.get('windWidth') / 2.0;
	}.property('windWidth'),

	transformG: function() {
		return "translate(" + this.get('margin.left') + "," + this.get('margin.top') + ")";
	}.property(),

	transformX: function() {
		return "translate(0,"+ this.get('h') +")";
	}.property('h'),

	transformWind: function() {
		return "translate(" + (this.get('tempWidth') + this.get('padding')) + "," + this.get('h') + ")";
	}.property('h'),

	draw: function() {
		var height = this.get('h');
		var data = this.get('data');
		var units = this.get('units');
		var tempWidth = this.get('tempWidth');
		var windWidth = this.get('windWidth');
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
			.orient('left');
		var windAxis = d3.svg.axis()
			.scale(windScale)
			.orient('bottom')
			.ticks(4);

		var line = d3.svg.line()
			.x(function(d) {
				return tempScale(convert(units, 'temperature', d['t']).value);
			})
			.y(function(d) {
				return altScale(convert(units, 'altitude', d['h']).value) - height;
			})
			.interpolate('linear');

		var wind = d3.svg.line()
			.x(function(d) {
				return windScale(convert(units, 'highSpeed', d['ws']).value);
			})
			.y(function(d) {
				return altScale(convert(units, 'altitude', d['h']).value) - height;
			})
			.interpolate('linear');

		svg.select('.temperature > .data').attr('d', line(data));
		svg.select('.wind > .data').attr('d', wind(data));
		svg.select('.wind > .direction')
			.selectAll('text')
			.data(data, function(d) {
				return d['wd'];
			})
			.enter()
			.append('text')
			.attr('font-family', 'weathericons')
			.attr('dy', '.35em')
			.attr('transform', function(d) {
				var x = windScale(convert(units, 'highSpeed', d['ws']).value) - 10;
				var y = altScale(convert(units, 'altitude', d['h']).value) - height;
				return 'translate(' + x + ',' + y + '), rotate(' + d['wd'] + ')';
			})
			.text('\uf058');
		svg.select('.temperature .axis')
			.call(tempAxis);
		var tempOffset = svg.select('.axis.altitude')
			.call(altAxis)
			.node()
			.getBBox().width;
		svg.select('.altitude .axis-label')
			.attr('y', -(tempOffset - 10));
		svg.select('.wind .axis')
			.call(windAxis);
	}.observes('units'),

	didInsertElement: function() {
		this.draw();
	}
});
