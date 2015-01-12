import DS from 'ember-data';
import Ember from 'ember';

export default DS.Transform.extend({
  serialize: function(value) {
		var ser = {
			type: 'Point',
			coordinates: [
				value.get('longitude'), value.get('latitude')
			]
		};
		var alt = value.get('altitude');
		var ts = value.get('time');
		if(isNaN(alt) === false) {
			ser['coordinates'].push(alt);
			if(isNaN(ts) === false) {
				ser['coodinates'].push(ts);
			}
		}
		return ser;
  },

  deserialize: function(value) {
		var lon = value['coordinates'][0];
		var lat = value['coordinates'][1];
		var alt = value['coordinates'][2] || NaN;
		var ts = value['coordinates'][3] || NaN;
    return Ember.create({
			longitude: lon, latitude: lat, altitude: alt, time: ts
		});
  }
});
