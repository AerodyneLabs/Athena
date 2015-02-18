import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    runPrediction: function() {
      var controller = this;
      var launchTime = new Date(this.get('launchTimeInput'));
      var locationTokens = this.get('launchLocationInput').split(',');
      var launchLocation = Ember.create({
        longitude: Number(locationTokens[1]),
        latitude: Number(locationTokens[0])
      });
      var prediction = this.store.createRecord('prediction', {
        launchTime: launchTime,
        launchLocation: launchLocation
      });
      prediction.save().then(function(prediction) {
        controller.transitionToRoute('prediction.detail', prediction);
      });
    }
  }
});
