"use strict";

/**
 * Modal GEO picker 
 * @memberof Geo
 * @ngdoc service
 * @name GeoPickerModal 
 */

const angular = require("angular");
const template = require("geo/picker.html");

const factory = function ($q, $modal, GeoService) {

    const modalCtl = [
        "$scope",
        "NgMap",
        "countries",
        "geodata",
    function ($scope, NgMap, countries, geodata) {

        const updateRegions = function () {
            if (!$scope.values.country) {
                $scope.choices.regions = [];
                return;
            }

            return GeoService.getRegions($scope.values.country.id)
                .then((regions) => {
                    $scope.choices.regions = regions; 
                });
        };

        const updateCities = function () {
            let {region, country} = $scope.values;

            if (!country || !region) {
                $scope.choices.cities = [];
                return;
            }

            return GeoService.getCities(country.id, region.id)
                .then((cities) => {
                    $scope.choices.cities = cities;
                });

        };

        const loadRequirement = function () {
            if ($scope.values.country) {
                return updateRegions()
                    .then(() => {
                        if ($scope.values.region) {
                            return updateCities();
                        }
                    });
            }
        };

        const getMap = function () {
            return $q((resolve) => {
                if ($scope.map) {
                    return resolve($scope.map);
                } else {
                    $scope.mapDefer.promise.then(resolve);
                }
            });
        };

        const loadMap = function () {
            return NgMap.getMap()
                .then((map) => {
                    $scope.map = map;
                    $scope.mapDefer.resolve(map);
                });
        };

        $scope.choices = {
            countries: countries,
            regions: [],
            cities: [],
        };

        $scope.values = {
            country: geodata.country || null,
            region: geodata.region || null,
            city: geodata.city || null,
            address: geodata.address || null,
        };


        $scope.map = null;
        $scope.mapDefer = $q.defer();

        $scope.addressChange = function () {
            let place = this.getPlace();
            console.log("Address, change", place);
            getMap()
                .then((map) => {
                    map.setCenter(place.geometry.location);
                });
        };

        $scope.$watchCollection("values.country", () => {
            return updateRegions();
        });

        $scope.$watchCollection("values.region", () => {
            return updateCities(); 
        });

        $scope.$watchCollection("values.city", () => {

            if (!$scope.values.city) {
                return;
            }

            getMap()
                .then((map) => {
                    map.setCenter({
                        lat: parseFloat($scope.values.city.latitude),
                        lng: parseFloat($scope.values.city.longitude),
                    });
                });
        });

        $scope.dirtForm = function (form) {
            if (form.$error && form.$error.required) {
                form.$error.required.forEach((f) => {
                    f.$setDirty(); 
                });
            }

            return form;
        };

        $scope.ok = function (form) {
            var data;

            $scope.dirtForm(form);

            if (form.$invalid) {
                return;
            }

            data = angular.copy($scope.values);
            $scope.$close(data);
            
        };
        
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

        return $q.all([
            loadRequirement(),
            loadMap(),
        ]);

    }];

    const open = function(geodata = {}, options = {}) {

        var modal = $modal.open({
            template,
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                geodata() {
                    return GeoService.resolveData(geodata);
                },
                options() {
                    return options;
                },
                countries() {
                    return GeoService.getCountries();
                },
            },
        });

        return modal;

    };

    return {
        open,
    };

};

module.exports = [
    "$q",
    "$modal",
    "GeoService",
    factory,
];
