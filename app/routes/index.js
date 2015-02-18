import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return Ember.RSVP.hash({
      currentFlights: this.store.find('flight', {status: 'current'}),
      upcomingFlights: this.store.find('flight', {status: 'upcoming'})
    });
  }
});
