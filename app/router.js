import Ember from "ember";
import config from "./config/environment";

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route("about");

  this.route("forecastPeriods");
  this.route("forecastPeriod", {
    path: "/foreastPeriod/:id"
  });

  this.route("soundings");
  this.route("sounding", {
		path: "/sounding/:id"
	});
});

export default Router;
