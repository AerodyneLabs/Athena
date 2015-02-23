import Ember from 'ember';

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
      var lat = this.parseLocation(this.get('latitudeInput'));
      var lon = this.parseLocation(this.get('longitudeInput'));
      if(this.setLocation([lon, lat])) {
        this.transitionToRoute('prediction.wizard.2');
      }
    },
    search: function() {
      var controller = this;
      controller.set('searchIcon', 'spinner');
      controller.set('searching', true);
      Ember.$.get('api/geo/address', {
        address: this.get('searchInput')
      }).done(function(data) {
        controller.set('searchError', false);
        controller.setLocation(data.location.coordinates);
      }).fail(function() {
        controller.set('searchError', true);
      }).always(function() {
        controller.set('searching', false);
        controller.set('searchIcon', 'search');
      });
    }
  },
  parseLocation: function(loc) {
    // Empty strings are invalid
    if(loc === '') {
      return NaN;
    }
    // Attempt to convert the string
    var value = Number(loc);
    // If conversion was successful we are done
    if(!isNaN(value)) {
      return value;
    }
    // Remove the hemisphere key
    var hemi = loc.slice(-1);
    if(hemi === 'N' || hemi === 'E') {
      hemi = 1;
    } else if(hemi === 'S' || hemi === 'W') {
      hemi = -1;
    } else {
      return NaN;
    }
    // Attempt to determine the delimiter
    var delim = ' ';
    if(loc.indexOf('-') > 0) {
      delim = '-';
    }
    // Split the string into fields
    var tokens = loc.slice(0, -1).split(delim);
    // Convert the degree field
    value = Number(tokens[0]);
    // Convert the minutes field
    var minutes = Number(tokens[1]);
    if(isNaN(minutes)) {
      return NaN;
    }
    value += minutes / 60.0;
    //Convert the seconds field
    if(tokens[2]) {
      var seconds = Number(tokens[2]);
      if(isNaN(seconds)) {
        return NaN;
      }
      value += seconds / 3600.0;
    }
    // Apply the hemisphere sign
    value *= hemi;

    return value;
  },
  setLocation: function(loc) {
    var latitude = loc[1];
    var longitude = loc[0];
    if(latitude <= 90.0 && latitude >= -90.0) {
      this.set('latitudeInput', latitude);
    } else {
      return false;
    }
    if(longitude <= 180.0 && longitude > -180.0) {
      this.set('longitudeInput', longitude);
    } else {
      return false;
    }
    this.set('controllers.prediction/wizard.location', Ember.create({
      longitude: longitude,
      latitude: latitude
    }));
    return true;
  }
});
