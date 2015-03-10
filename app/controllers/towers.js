import Ember from 'ember';
import Paginated from 'athena/mixins/paginated';

export default Ember.Controller.extend(Paginated, {
  total: function() {
    return this.store.metadataFor('tower').total;
  }.property('model')
});
