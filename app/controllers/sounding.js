import Ember from 'ember';

export default Ember.ObjectController.extend({
  needs: ['application'],

  profile: function() {
    var model = this.get('model.profile');
    for(var i = 0; i < model.length; i++) {
      var obs = model[i];
      var u = obs.u;
      var v = obs.v;
      obs['ws'] = Math.sqrt(Math.pow(u, 2) + Math.pow(v, 2));
      var dir = Math.atan2(u, v) * 180.0 / Math.PI;
      if(dir < 0) {
        dir = dir + 360.0;
      }
      obs['wd'] = dir;
    }
    return model;
  }.property('model.profile')
});
