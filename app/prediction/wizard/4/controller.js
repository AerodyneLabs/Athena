import Ember from 'ember';

export default Ember.Controller.extend({
  time: '',
  date: '',
  needs: ['prediction/wizard'],
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.3');
    },
    run: function() {
      console.log('Run prediction');
    }
  }
});