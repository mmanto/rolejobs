"use strict";

/**
 * Postulant panel, postulations
 * @memberof Postulants
 * @ngdoc service
 * @name PostulantFavoritesService
 */

const factory = function (CollectionService) {

    const getCollection = function () {
        const path = "postulant/panel/favorites";
        return new CollectionService.Collection(path);
    };

    return {
        getCollection,
    };

};

module.exports = [
    "CollectionService",
    factory
];
