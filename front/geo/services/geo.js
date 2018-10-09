"use strict";

const angular = require("angular");

/**
 * Geo service 
 * @memberof Geo 
 * @ngdoc service 
 * @name GeoService 
 */ 

const factory = function ($q, Api) {

    const get = function (relpath, params = {}) {
        var path = `geo/${relpath}`;

        return Api.getInstance().get(path, params) 
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Invalid response");
                }
            });
    };

    const getCountries = function () {
        return get("countries"); 
    };

    const getCountry = function (country) {
        return get(`countries/${country}`);
    };

    const getRegions = function (country) {
        return get(`countries/${country}/regions`);
    };

    const getRegion = function (country, region) {
        return get(`countries/${country}/regions/${region}`);
    };

    const getCities = function (country, region) {
        return get(`countries/${country}/regions/${region}/cities`);
    };

    const getCity = function (country, region, city) {
        return get(`countries/${country}/regions/${region}/cities/${city}`);
    };

    const resolveData = function (geodata = {}) {

        return $q.when(angular.copy(geodata))
            .then((rdata) => {
                let {country} = rdata;

                if (country && typeof country !== "object") {
                    return getCountry(country)
                        .then((dcountry) => {
                            rdata.country = dcountry;
                            return rdata;
                        })
                        .catch((e) => {
                            throw e;
                        });
                } else {
                    return rdata;
                } 

            })
            .then((rdata) => {
                let {country, region} = rdata;

                if (country && region && typeof region !== "object") {
                    return getRegion(country.id, region)
                        .then((dregion) => {
                            rdata.region = dregion;
                            return rdata;
                        })
                        .catch((e) => {
                            throw e;
                        });
                } else {
                    return rdata;
                }

            })
            .then((rdata) => {
                let {country, region, city} = rdata;

                if (region && city && typeof city !== "object") {
                    return getCity(
                        country.id, region.id, city)
                        .then((dcity) => {
                            rdata.city = dcity;
                            return rdata;
                        })
                        .catch((e) => {
                            throw e;
                        });
                } else {
                    return rdata;
                }

            });

    };

    return {
        getCountries,
        getCountry,
        getRegions,
        getRegion,
        getCities,
        getCity,
        resolveData,
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    factory
];
