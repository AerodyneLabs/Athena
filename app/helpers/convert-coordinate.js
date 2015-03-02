import Ember from 'ember';

export function convertCoordinate(value, style, type) {
  var d, m, s, ret;
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

export default Ember.Handlebars.makeBoundHelper(convertCoordinate);
