import Ember from 'ember';

export default Ember.Controller.extend({
  needs: ['prediction/wizard'],
  actions: {
    next: function() {
      this.transitionToRoute('prediction.wizard.2');
    }
  }
});
