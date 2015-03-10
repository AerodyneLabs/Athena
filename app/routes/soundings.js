import PaginationBase from 'athena/routes/pagination-base';

/**
 * A route to display a list of all soundings
 * @class SoundingsRoute
 * @extends PaginationBase
 */
export default PaginationBase.extend({
	init: function() {
		this._super('sounding');
	}
});
