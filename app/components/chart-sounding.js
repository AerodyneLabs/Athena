import Ember from 'ember';
import convert from 'athena/helpers/units';

export default Ember.Component.extend({
	tagName: 'svg',
	attributeBindings: 'width height'.w(),

	margin: {top: 20, right: 20, bottom: 40, left: 80},
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
		var width = this.get('w');
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

		var altitude = function(d) {
			return altScale(convert(units, 'altitude', d['h']).value) - height;
		};

		var line = d3.svg.line()
			.x(function(d) {
				return tempScale(convert(units, 'temperature', d['t']).value);
			})
			.y(altitude)
			.interpolate('linear');

		var wind = d3.svg.line()
			.x(function(d) {
				return windScale(convert(units, 'highSpeed', d['ws']).value);
			})
			.y(altitude)
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
				var x = windScale(convert(units, 'highSpeed', d['ws']).value);
				var y = altitude(d);
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
		var grid = svg.select('.grid');
		grid.select('.altitude')
			.selectAll('line')
			.data(altScale.ticks())
			.enter()
			.append('line')
			.attr('x1', 0)
			.attr('x2', width)
			.attr('y1', function(d) {
				return altScale(d);
			})
			.attr('y2', function(d) {
				return altScale(d);
			});
		grid.select('.temperature')
			.selectAll('line')
			.data(tempScale.ticks(5))
			.enter()
			.append('line')
			.attr('y1', 0)
			.attr('y2', height)
			.attr('x1', function(d) {
				return tempScale(d);
			})
			.attr('x2', function(d) {
				return tempScale(d);
			});
		grid.select('.wind')
			.selectAll('line')
			.data(windScale.ticks(3))
			.enter()
			.append('line')
			.attr('y1', 0)
			.attr('y2', -height)
			.attr('x1', function(d) {
				return windScale(d);
			})
			.attr('x2', function(d) {
				return windScale(d);
			});

		var bisectAlt = d3.bisector(function(a, b) {
			return b - convert(units, 'altitude', a['h']).value;
		}).left;

		var focus = svg.select('.focus')
			.style('display', 'none');

		svg.select('rect.overlay')
			.on('mouseover', function() {
				focus.style('display', null);
			})
			.on('mouseout', function() {
				focus.style('display', 'none');
			})
			.on('mousemove', mousemove);

		function mousemove() {
			var y0 = altScale.invert(d3.mouse(this)[1]);
			var i = bisectAlt(data, y0, 1);
			var d0 = data[i -1];
			var d1 = data[i];
			var d = y0 - d0['h'] < d1['h'] - y0 ? d1 : d0;
			var y = altitude(d);
			focus.attr('transform', 'translate(0,' + (y + height) + ')');
			var altRes = convert(units, 'altitude', d['h']);
			var tempRes = convert(units, 'temperature', d['t']);
			var presRes = convert(units, 'pressure', d['p']);
			var windRes = convert(units, 'highSpeed', d['ws']);
			var alt = altRes.value + ' ' + altRes.unit;
			var temp = tempRes.value + ' ' + tempRes.unit;
			var pres = presRes.value + ' ' + presRes.unit;
			var wind = windRes.value + ' ' + windRes.unit;
			focus.select('text')
				.text(alt + ' ' + temp + ' ' + pres + ' ' + wind);
		}
	}.observes('units'),

	didInsertElement: function() {
		this.draw();
	}
});
