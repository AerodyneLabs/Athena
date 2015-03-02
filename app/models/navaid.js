import DS from 'ember-data';

export default DS.Model.extend({
  type: DS.attr('string'),
  geometry: DS.attr('point'),
  properties: DS.attr()
});
