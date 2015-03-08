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
      var controller = this;
      var model = controller.store.createRecord('prediction', {
        launchTime: new Date(),
        launchLocation: Ember.create({
          latitude: 42,
          longitude: -93
        })
      });
      model.save().then(function(prediction) {
        controller.transitionToRoute('prediction.detail', prediction);
      });
    }
  }
});
