import Ember from "ember";
import config from "./config/environment";

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.resource("about", function() {});
  this.resource("forecastPeriods", function() {});
  this.resource("forecastPeriod", {path: "/forecastPeriod/:id"}, function() {});
});

export default Router;
