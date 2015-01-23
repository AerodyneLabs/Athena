import DS from 'ember-data';

/**
 * Customize data store serialization application wide
 * @class ApplicationSerializer
 * @extends DS.RESTSerializer
 */
export default DS.RESTSerializer.extend({
	/**
	 * Define the data store backend primary key
	 * @property primaryKey
	 * @type String
	 */
	primaryKey: '_id'
});
