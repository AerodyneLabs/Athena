import DateTimePicker from 'ember-bootstrap-datetimepicker/components/bs-datetimepicker';

export function initialize(/* container, application */) {
  DateTimePicker.reopen({
    icons: {
      time: 'fa fa-clock-o',
      date: 'fa fa-calendar',
      up: 'fa fa-chevron-up',
      down: 'fa fa-chevron-down',
      previous: 'fa fa-chevron-left',
      next: 'fa fa-chevron-right'
    }
  });
}

export default {
  name: 'bs-date-time-picker',
  initialize: initialize
};
