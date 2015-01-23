import DS from 'ember-data';
import Ember from 'ember';

/**
 * Transform an array between the data store and the backend
 * @class ArrayTransform
 * @extends DS.Transform
 */
export default DS.Transform.extend({
	/**
	 * Deserialize a JSON string as an Ember model array attribute
	 * @method deserialize
	 * @param serialized {JSON} JSON string to be deserialized
	 * @return {Array} Deserialized Ember model array attribute
	 */
	deserialize: function(serialized) {
		return (Ember.typeOf(serialized) === 'array') ? serialized : [];
  },

	/**
	 * Serialize an Ember model array attribute as a JSON string
	 * @method serialize
	 * @param deserialized {Array} Ember model array attribute to be serialized
	 * @return {JSON} Serialized JSON string
	 */
  serialize: function(deserialized) {
		var type = Ember.typeOf(deserialized);
		if(type === 'array') {
			return deserialized;
		} else if(type === 'string') {
			return deserialized.split(',').map(function(item) {
				return Ember.$.trim(item);
			});
		} else {
			return [];
		}
  }
});
