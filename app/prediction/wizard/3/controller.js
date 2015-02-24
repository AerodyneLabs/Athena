import Ember from 'ember';

export default Ember.Controller.extend({
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
