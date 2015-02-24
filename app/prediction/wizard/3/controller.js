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
    'Fruity Elliptical 24"': {area: 24, drag: 1.5},
    'Fruity Elliptical 30"': {area: 30, drag: 1.5},
    'Fruity Elliptical 36"': {area: 36, drag: 1.5},
    'Fruity Elliptical 42"': {area: 42, drag: 1.5},
    'Fruity Elliptical 48"': {area: 48, drag: 1.5},
    'Fruity Elliptical 60"': {area: 60, drag: 1.5}
  },
  parachuteArea: 0,
  parachuteDrag: 0,
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
    var chuteData = this.parachuteData[chute];
    this.set('parachuteArea', chuteData.area);
    this.set('parachuteDrag', chuteData.drag);
  }.observes('parachute'),
  needs: ['prediction/wizard'],
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.2');
    },
    next: function() {
      this.transitionToRoute('prediction.wizard.4');
    }
  }
});
