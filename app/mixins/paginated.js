import Ember from 'ember';

export default Ember.Mixin.create({
  queryParams: ['page'],
  page: 1,
  offset: 0,
  pageCount: function() {
    var total = this.get('total');
    var limit = this.get('limit');
    return Math.ceil(total / limit);
  }.property('total', 'limit'),
  actions: {
    changePage: function(page) {
      this.transitionToRoute('towers', {queryParams: {page: page}});
    }
  }
});
