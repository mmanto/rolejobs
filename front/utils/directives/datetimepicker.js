"use strict";

/**
 * DatetimePicker implementation with angular
 * @memberof Utils
 * @ngdoc directive
 * @name datetimepicker 
 */

const jQuery = require('jquery');

const datetimepickerFactory = function () {

    return {
        strict: "EA",
        link: function(scope, element) {

            var e = jQuery(element[0]);

            e.datepicker({
                dateFormat: "yy-mm-dd",
                altFormat: "yy-mm-dd",
                onSelect: function(dateText) {
                var modelPath = $(this).attr('ng-model');
                //putObject(modelPath, scope, dateText);
                scope.$apply();
                }
            });

        }
    };

};

module.exports = datetimepickerFactory;
