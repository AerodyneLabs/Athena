import Ember from 'ember';
import moment from 'moment';

export default Ember.Controller.extend({
  time: moment(),
  timeError: false,
  needs: ['prediction/wizard'],
  actions: {
    back: function() {
      this.transitionToRoute('prediction.wizard.3');
    },
    run: function() {
      if(this.validate()) {
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
  },
  validate: function() {
    var valid = true;

    var time = this.get('time');
    console.log(time.toDate());
    if(!time.isValid() || time.isBefore()) {
      valid = false;
      this.set('timeError', true);
    } else {
      this.set('timeError', false);
    }

    return valid;
  }
});
