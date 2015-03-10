import Ember from 'ember';

export default Ember.Route.extend({
  offset: 0,
  limit: 25,
  queryParams: {
    page: {
      refreshModel: true
    }
  },
  init: function(domain) {
    this._super();
    this.set('domain', domain);
  },
  model: function(params) {
    var page = 1;

    if(params.page) {
      page = params.page;
      page = isNaN(page) ? 1 : Math.floor(Math.abs(page));
      this.set('offset', (page - 1) * this.get('limit'));
    }

    return this.store.find(this.get('domain'), {
      offset: this.get('offset'),
      limit: this.get('limit')
    });
  },
  setupController: function(controller, model) {
    this._super(controller, model);
    controller.setProperties({
      offset: this.get('offset'),
      limit: this.get('limit')
    });
  }
});
