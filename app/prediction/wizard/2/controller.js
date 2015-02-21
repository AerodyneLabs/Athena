import Ember from 'ember';

export default Ember.Controller.extend({
  needs: ['prediction/wizard'],
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.1');
    },
    next: function() {
      this.transitionToRoute('prediction.wizard.3');
    }
  }
});
