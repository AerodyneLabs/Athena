import Ember from 'ember';
import PaginatedMixin from '../../../mixins/paginated';
import { module, test } from 'qunit';

module('PaginatedMixin');

// Replace this with your real tests.
test('it works', function(assert) {
  var PaginatedObject = Ember.Object.extend(PaginatedMixin);
  var subject = PaginatedObject.create();
  assert.ok(subject);
});
