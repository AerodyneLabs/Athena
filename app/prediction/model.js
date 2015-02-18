import DS from 'ember-data';

export default DS.Model.extend({
  launchTime: DS.attr('date'),
  launchLocation: DS.attr('point')
});
