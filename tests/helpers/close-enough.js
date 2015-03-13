import QUnit from 'qunit';

console.log('imported closeEnough');

export default function(actual, expected, message) {
  var diff = Math.abs(actual - expected);
  var res = diff < 0.001;
  QUnit.push(res, actual, expected, message);
}
