"use strict";

const angular = require("angular");

/**
 * Geo field, with forms utils 
 * @memberof Geo 
 * @ngdoc directive
 * @name geoField 
 */

const factory = function (GeoService, GeoModal) {

    const DISPLAY_NAME = "display_name";

    return {
        strict: "EA",
        repace: true,
        template: `<span class="geo-field" ng-click="edit()">
                     <i class="fa fa-map-marker"></i>
                     <span class="geoname">{{geoname}}</span>
                     <span ng-show="!data" class="placeholder">
                        {{placeholder}}
                     </span>
                   </span>`,
        require: '?ngModel', 
        scope: {

            localDelegate: '=myDelegate'
        },
        link: (scope, element, attrs, ngModel) => {
            scope.data = {};
            scope.geoname = "...";
            scope.placeholder = attrs.placeholder || "";

            // Upate view with the new geoname 
            const updateInfo = function () {

                if (!scope.data) {
                    scope.geoname = "";
                    return;
                }

                let {address, country, region, city} = scope.data;
                let geoname = "";

                if (address) {
                    geoname += address;
                }

                if (city) {
                    geoname += `, ${city[DISPLAY_NAME]}`;
                } else if (region) {
                    geoname += `, ${region[DISPLAY_NAME]}`; 
                } else if (country) {
                    geoname += `, ${country.name}`;
                }

                scope.geoname = geoname;

            };

            // Set the data (from modal)
            const setData = function (rdata) {
                debugger;
                scope.data = rdata;
                let {address, country, region, city} = rdata;
                let vdata;

                updateInfo();

                if (ngModel) {

                    ngModel.$setDirty();
                    ngModel.$setTouched();

                    if (region || city) {
                        
                        vdata = ngModel.$viewValue || {};

                        ngModel.$setViewValue(angular.extend(vdata, {
                            address,
                            country: country ? country.id : null,
                            region: region ? region.id : null,
                            city: city ? city.id : null
                        }));
                    } else {
                        ngModel.$setViewValue(null);
                    }

                }

                scope.localDelegate.changeGeoData(ngModel.$modelValue);

            };

            // Update data from model
            const updateData = function (vdata) {

                if (!vdata) {
                    scope.data = null;
                    return updateInfo();
                }
            
                return GeoService.resolveData(vdata)
                    .then((rdata) => {
                        scope.data = rdata;
                        updateInfo();
                    });

            };

            // When tag is clicked, open selection modal
            scope.edit = function () {
                let modal = GeoModal.open(scope.data || {});
                modal.result.then((rdata) => {
                    setData(rdata);
                });
            };

            if (ngModel) {
                ngModel.$render = function () {
                    updateData(ngModel.$viewValue);
                };

                updateData(ngModel.$modelValue);
            }

        }
    };

};

module.exports = [
    "GeoService",
    "GeoPickerModal",
    factory
];
