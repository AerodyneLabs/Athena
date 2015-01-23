import DS from "ember-data";

/**
 * Customize the data store behavior application wide
 * @class ApplicationAdapter
 * @extends DS.RESTAdapter
 */
export default DS.RESTAdapter.extend({
	/**
	 * Define the data store backend namespace
	 * @propery namespace
	 * @type String
	 */
	namespace: 'api'
});
