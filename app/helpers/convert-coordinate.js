import Ember from 'ember';

export function convertCoordinate(value, style, type, inverse) {
  var d, m, s, ret;
  if(inverse) {
    // Empty strings are invalid
    if(value === '') {
      return NaN;
    }
    // Attempt to convert the string
    ret = Number(value);
    // If conversion was successful we are done
    if(!isNaN(ret)) {
      return ret;
    }
    // Remove the hemisphere key
    var hemi = value.slice(-1);
    if(hemi === 'N' || hemi === 'E') {
      hemi = 1;
    } else if(hemi === 'S' || hemi === 'W') {
      hemi = -1;
    } else {
      return NaN;
    }
    // Attempt to determine the delimiter
    var delim = ' ';
    if(value.indexOf('-') > 0) {
      delim = '-';
    }
    // Split the string into fields
    var tokens = value.slice(0, -1).split(delim);
    // Convert the degree field
    ret = Number(tokens[0]);
    // Convert the minutes field
    if(tokens[1]) {
      var minutes = Number(tokens[1]);
      if(isNaN(minutes)) {
        return NaN;
      }
      ret += minutes / 60.0;
    }
    //Convert the seconds field
    if(tokens[2]) {
      var seconds = Number(tokens[2]);
      if(isNaN(seconds)) {
        return NaN;
      }
      ret += seconds / 3600.0;
    }
    // Apply the hemisphere sign
    ret *= hemi;

    return ret;
  } else {
    if(style === 'DMS') {
      d = ~~value;
      m = ~~(Math.abs(value) * 60) % 60;
      s = (Math.abs(value) * 3600) % 60;
      ret = Math.abs(d) + '-' + m + '-' + s.toFixed(4);
      if(type === 'latitude') {
        if(d >= 0) {
          ret += 'N';
        } else {
          ret += 'S';
        }
      } else {
        if(d >= 0) {
          ret += 'E';
        } else {
          ret += 'W';
        }
      }
      return ret;
    } else if(style === 'DM') {
      d = ~~value;
      m = Math.abs(value - d) * 60;
      ret = Math.abs(d) + '-' + m.toFixed(6);
      if(type === 'latitude') {
        if(d >= 0) {
          ret += 'N';
        } else {
          ret += 'S';
        }
      } else {
        if(d >= 0) {
          ret += 'E';
        } else {
          ret += 'W';
        }
      }
      return ret;
    } else {
      return value;
    }
  }
}

export default Ember.Handlebars.makeBoundHelper(convertCoordinate);
