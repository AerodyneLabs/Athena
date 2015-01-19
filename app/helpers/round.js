export default function roundNumber(value, digits) {
  var val = Number(value);
  var dig = Number(digits);
  return Number(Math.round(val + 'e' + (-dig)) + ('e' + dig));
}
