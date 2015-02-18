import DS from 'ember-data';
import Ember from 'ember';

/**
 * Transform a geographic location between the data store and backend
 * @class PointTransform
 * @extends DS.Transform
 */
export default DS.Transform.extend({
  /**
   * Serialize an Ember model point attribute as a GeoJSON point
   * @method serialized
   * @param deserialized {Point} Ember model point attribute to be serialized
   * @return {JSON} GeoJSON serialized point
   */
  serialize: function(deserialized) {
    console.log('serialize: ', deserialized);
		var ser = {
			type: 'Point',
			coordinates: [
				deserialized.longitude, deserialized.latitude
			]
		};
    /*
		var alt = deserialized.get('altitude');
		var ts = deserialized.get('time');
		if(isNaN(alt) === false) {
			ser['coordinates'].push(alt);
			if(isNaN(ts) === false) {
				ser['coodinates'].push(ts);
			}
		}*/
		return ser;
  },

  /**
   * Deserialize a GeoJSON point as an Ember model point attribute
   * @method deserialize
   * @param serialized {JSON} GeoJSON serialized point
   * @return {Point} Ember model point attrbute
   */
  deserialize: function(serialized) {
		var lon = serialized['coordinates'][0];
		var lat = serialized['coordinates'][1];
		var alt = serialized['coordinates'][2] || NaN;
		var ts = serialized['coordinates'][3] || NaN;
    return Ember.create({
			longitude: lon, latitude: lat, altitude: alt, time: ts
		});
  }
});
