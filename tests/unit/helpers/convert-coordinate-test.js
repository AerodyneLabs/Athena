import {
  convertCoordinate
} from '../../../helpers/convert-coordinate';
import { module, test } from 'qunit';
import closeEnough from '../../helpers/close-enough';

module('ConvertCoordinateHelper');

test('inverts from signed decimal degrees', function() {
  closeEnough(convertCoordinate('40.4461', null, null, true), 40.4461);
  closeEnough(convertCoordinate('-79.9822', null, null, true), -79.9822);
});

test('inverts from decimal degrees', function() {
  closeEnough(convertCoordinate('40.4461N', null, null, true), 40.4461);
  closeEnough(convertCoordinate('79.9822W', null, null, true), -79.9822);
});

test('inverts from decimal minutes', function(assert) {
  closeEnough(convertCoordinate('40-26.767N', null, null, true), 40.4461);
  closeEnough(convertCoordinate('79-58.933W', null, null, true), -79.9822);
});

test('inverts from degrees-minutes-seconds', function() {
  closeEnough(convertCoordinate('40-26.767N', null, null, true), 40.4461);
  closeEnough(convertCoordinate('79-58.933W', null, null, true), -79.9822);
});
