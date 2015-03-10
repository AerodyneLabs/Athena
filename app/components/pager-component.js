import Ember from 'ember';

export default Ember.Component.extend({
  pageCount: 1,
  currentPage: 1,
  excessPages: 2,
  pages: function() {
    var pageCount = this.get('pageCount');
    var excessPages = this.get('excessPages');
    var currentPage = this.get('currentPage');
    var minPage = 1;
    var maxPage = pageCount;
    if(currentPage < (excessPages + 1)) {
      maxPage = Math.min(2 * excessPages + 1, pageCount);
    } else if(currentPage > (pageCount - excessPages)) {
      minPage = Math.max(pageCount - 2 * excessPages, 1);
    } else {
      minPage = currentPage - excessPages;
      maxPage = currentPage + excessPages;
    }
    var pages = [];
    for(var i = minPage; i <= maxPage; i++) {
      var classes = '';
      if(i === currentPage) {
        classes = 'active';
      }
      pages.push({key: i, classes: classes});
    }
    return pages;
  }.property('pageCount', 'currentPage'),
  first: function() {
    if(this.get('currentPage') <= 1) {
      return true;
    } else {
      return false;
    }
  }.property('pageCount', 'currentPage'),
  last: function() {
    if(this.get('currentPage') >= this.get('pageCount')) {
      return true;
    } else {
      return false;
    }
  }.property('pageCount', 'currentPage'),
  actions: {
    prev: function() {
      var curPage = this.get('currentPage');
      this.sendAction('action', curPage - 1);
    },
    next: function() {
      var curPage = this.get('currentPage');
      this.sendAction('action', curPage + 1);
    },
    page: function(page) {
      this.sendAction('action', page);
    }
  }
});
