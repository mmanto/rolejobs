"use strict";

/**
 * Postulant panel, postulations
 * @memberof Postulants
 * @ngdoc service
 * @name PostulantMessagesService
 */

const factory = function (CollectionService) {

    const getCollection = function () {
        const path = "postulant/panel/messages";
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
