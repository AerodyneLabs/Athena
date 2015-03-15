import Ember from 'ember';
import {convertCoordinate} from 'athena/helpers/convert-coordinate';

export default Ember.Controller.extend({
  searchError: false,
  searchIcon: 'search',
  searching: false,
  latitudeError: false,
  longitudeError: false,
  searchInput: '',
  latitudeInput: '',
  longitudeInput: '',
  needs: ['prediction/wizard'],
  actions: {
    next: function() {
      var goodLat = false;
      var lat = convertCoordinate(this.get('latitudeInput'), null, null, true);
      if(isNaN(lat)) {
        this.set('latitudeError', true);
      } else if(lat > 90 || lat < -90) {
        this.set('latitudeError', true);
      } else {
        this.set('latitudeError', false);
        goodLat = true;
      }
      var goodLon = false;
      var lon = convertCoordinate(this.get('longitudeInput'), null, null, true);
      console.log(lat, lon);
      if(isNaN(lon)) {
        this.set('longitudeError', true);
      } else if(lon < -180 || lon > 180) {
        this.set('longitudeError', true);
      } else {
        this.set('longitudeError', false);
        goodLon = true;
      }
      if(goodLat && goodLon) {
        if(this.setLocation([lon, lat])) {
          this.transitionToRoute('prediction.wizard.2');
        }
      }
    },
    search: function() {
      var controller = this;
      controller.set('searchIcon', 'spinner');
      controller.set('searching', true);
      Ember.$.get('api/geo/address', {
        address: this.get('searchInput')
      }).done(function(data) {
        var coords = data.location.coordinates;
        if(coords) {
          controller.set('latitudeInput', coords[1]);
          controller.set('longitudeInput', coords[0]);
        } else {
          controller.set('searchError', true);
        }
        controller.set('searchError', false);
      }).fail(function() {
        controller.set('searchError', true);
      }).always(function() {
        controller.set('searching', false);
        controller.set('searchIcon', 'search');
      });
    }
  },
  setLocation: function(loc) {
    var latitude = loc[1];
    var longitude = loc[0];
    this.set('controllers.prediction/wizard.location', Ember.create({
      longitude: longitude,
      latitude: latitude
    }));
    return true;
  }
});
