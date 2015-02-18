import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  status: DS.attr('string'),
  launchTime: DS.attr('date'),
  launchLocation: DS.attr('point')
});
