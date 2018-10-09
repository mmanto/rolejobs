"use strict";

/**
 * Postulant panel, postulations
 * @memberof Postulants
 * @ngdoc service
 * @name PostulantPostulationsService
 */

const factory = function (CollectionService) {

    const getCollection = function () {
        const path = "postulant/panel/postulations";
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
