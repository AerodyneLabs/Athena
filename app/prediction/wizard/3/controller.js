import Ember from 'ember';

export default Ember.Controller.extend({
  parachute: 'Custom',
  parachutes: [
    'Custom',
    'Fruity Elliptical 24"',
    'Fruity Elliptical 30"',
    'Fruity Elliptical 36"',
    'Fruity Elliptical 42"',
    'Fruity Elliptical 48"',
    'Fruity Elliptical 60"'
  ],
  parachuteData: {
    'Fruity Elliptical 24"': {area: 0.2877, drag: 1.5},
    'Fruity Elliptical 30"': {area: 0.4, drag: 1.5},
    'Fruity Elliptical 36"': {area: 0.5626, drag: 1.5},
    'Fruity Elliptical 42"': {area: 0.751, drag: 1.5},
    'Fruity Elliptical 48"': {area: 0.9374, drag: 1.5},
    'Fruity Elliptical 60"': {area: 1.502, drag: 1.5}
  },
  parachuteArea: 0,
  parachuteDrag: 0,
  parachuteRadius: 0,
  parachuteSpillRadius: 0,
  isCustom: function() {
    if(this.get('parachute') === 'Custom') {
      return true;
    }
    return false;
  }.property('parachute'),
  isStatic: function() {
    if(this.get('parachute') === 'Custom') {
      return false;
    }
    return true;
  }.property('parachute'),
  parachuteChanged: function() {
    var chute = this.get('parachute');
    if(chute === 'Custom') {
      return;
    }
    var chuteData = this.parachuteData[chute];
    this.set('parachuteArea', chuteData.area);
    this.set('parachuteDrag', chuteData.drag);
  }.observes('parachute'),
  computeArea: function() {
    var r1 = this.get('parachuteRadius');
    var r2 = this.get('parachuteSpillRadius');
    var area = 3.1415 * ((r1 * r1) - (r2 * r2));
    this.set('parachuteArea', area);
  }.observes('parachuteRadius', 'parachuteSpillRadius'),
  needs: ['application', 'prediction/wizard'],
  units: Ember.computed.alias('controllers.application.units'),
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.2');
    },
    next: function() {
      this.transitionToRoute('prediction.wizard.4');
    }
  }
});
