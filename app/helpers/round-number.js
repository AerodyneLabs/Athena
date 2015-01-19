import Ember from 'ember';
import round from 'athena/helpers/round';

export function roundNumber(value, digits) {
  return round(value, digits);
}

export default Ember.Handlebars.makeBoundHelper(roundNumber);
