import Ember from 'ember';
import {convertLength} from 'athena/helpers/convert-length';

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
  parachuteError: false,
  parachuteRadiusError: false,
  parachuteSpillRadiusError: false,
  areaError: false,
  dragError: false,
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
    var unit = this.get('controllers.application.units.length');
    var chuteData = this.parachuteData[chute];
    var area = convertLength(convertLength(chuteData.area, unit), unit);
    this.set('parachuteArea', area);
    this.set('parachuteDrag', chuteData.drag);
  }.observes('parachute', 'controllers.application.units.length'),
  computeArea: function() {
    var valid = true;
    var r1 = this.get('parachuteRadius');
    if(isNaN(r1) || r1 <= 0) {
      valid = false;
      this.set('parachuteRadiusError', true);
    } else {
      this.set('parachuteRadiusError', false);
    }
    var r2 = this.get('parachuteSpillRadius');
    if(isNaN(r2) || r2 < 0) {
      valid = false;
      this.set('parachuteSpillRadiusError', true);
    } else {
      this.set('parachuteSpillRadiusError', false);
    }
    if(valid) {
      var area = 3.1415 * ((r1 * r1) - (r2 * r2));
      this.set('parachuteArea', area);
      this.set('areaError', false);
    } else {
      this.set('parachuteArea', 0);
      this.set('areaError', true);
    }
  }.observes('parachuteRadius', 'parachuteSpillRadius'),
  needs: ['application', 'prediction/wizard'],
  units: Ember.computed.alias('controllers.application.units'),
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.2');
    },
    next: function() {
      if(this.validate()) {
        this.transitionToRoute('prediction.wizard.4');
      }
    }
  },
  validate: function() {
    var valid = true;

    var chutes = this.get('parachutes');
    var chute = this.get('parachute');
    if(chutes.indexOf(chute) < 0) {
      valid = false;
      this.set('parachuteError', true);
    } else {
      this.set('parachuteError', false);
    }

    var area = this.get('parachuteArea');
    if(isNaN(area) || area <= 0) {
      valid = false;
      this.set('areaError', true);
    } else {
      this.set('areaError', false);
    }

    var drag = this.get('parachuteDrag');
    if(isNaN(drag) || drag <= 0) {
      valid = false;
      this.set('dragError', true);
    } else {
      this.set('dragError', false);
    }

    return valid;
  }
});
