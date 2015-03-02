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
      var goodLat = false;
      var lat = this.parseLocation(this.get('latitudeInput'));
      if(isNaN(lat)) {
        this.set('latitudeError', true);
      } else if(lat > 90 || lat < -90) {
        this.set('latitudeError', true);
      } else {
        this.set('latitudeError', false);
        goodLat = true;
      }
      var goodLon = false;
      var lon = this.parseLocation(this.get('longitudeInput'));
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
    this.set('controllers.prediction/wizard.location', Ember.create({
      longitude: longitude,
      latitude: latitude
    }));
    return true;
  }
});
