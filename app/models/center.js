import DS from 'ember-data';

export default DS.Model.extend({
  geometry: DS.attr(),
  properties: DS.attr(),
  type: DS.attr('string')
});
