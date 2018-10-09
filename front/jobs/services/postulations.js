"use strict";

/**
 * @memberof Jobs
 * @ngdoc service
 * @name PostulationsService
 */

const factory = function (CollectionService) {

    class OwnJobPostulationsRecordSet extends
                            CollectionService.CollectionRecordSet {
        
        _extendItem(item) {
            item = super._extendItem(item);
            item.$setStatus = (status) => {
                var path = `${item.id}`;
                return this.collection.put({status}, {}, path);
            };
            return item;
        }

    }

    class OwnJobPostulations extends CollectionService.Collection {

        constructor(jobId) {
            jobId = parseInt(jobId);
            super(`jobs/own/${jobId}/postulations`);
            this._jobId = jobId;
        }

        _getRecordSetClass() {
            return OwnJobPostulationsRecordSet;
        }
    
    }

    return {
        OwnJobPostulations
    };

};

module.exports = [
    "CollectionService",
    factory
];
