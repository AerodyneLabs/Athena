import Ember from 'ember';

export function convertCoordinate(value, style, type) {
  if(style === 'DMS') {
    var d = ~~value;
    var m = ~~(Math.abs(value) * 60) % 60;
    var s = (Math.abs(value) * 3600) % 60;
    var ret = Math.abs(d) + '-' + m + '-' + s.toFixed(4);
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
    var d = ~~value;
    var m = Math.abs(value - d) * 60;
    var ret = Math.abs(d) + '-' + m.toFixed(6);
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

export default Ember.Handlebars.makeBoundHelper(convertCoordinate);
