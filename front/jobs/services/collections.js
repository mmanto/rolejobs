"use strict";

/**
 * Jobs collection
 * @memberof Jobs
 * @ngdoc service
 * @name JobsCollections
 */

const factory = function (CollectionService) {

    var instances = {};

    class PublicJobRecordSet extends CollectionService.CollectionRecordSet {
        
        _extendItem(item) {
            item = super._extendItem(item);
            if (typeof item == 'object'){
                item.$postulate = (data) => {
                    var path = `${item.pk}/postulate`;
                    return this.collection.post(data, {}, path)
                        .then((result) => {
                            console.log("RESULT", result);
                        });
                };
            }
            return item;
        }

    }

    class JobsCollectionBase extends CollectionService.Collection {

        constructor(path) {
            if (typeof instances[path] !== "undefined") {
                throw new Error("Use getInstance");
            }

            super(`jobs/${path}`);
        }

        static getInstance() {
            if (typeof instances[this.name] === "undefined") {
                instances[this.name] = new this();
            }

            return instances[this.name];
        }

    } 

    class PublicJobs extends JobsCollectionBase {

        constructor(path = "jobs") {
            super(path);
        }

        _getRecordSetClass() {
            return PublicJobRecordSet;
        }

    }

    class OwnJobs extends JobsCollectionBase {

        constructor() {
            super("own");
        }

    }

    class ByArea extends PublicJobs {

        constructor(areaId) {
            areaId = parseInt(areaId);
            super(`jobs/by_area/${areaId}`);
            this._areaId = areaId; 
        }

        static getInstance(areaId) {
            if (typeof instances[`${this.name}:${areaId}`] === "undefined") {
                instances[`${this.name}:${areaId}`] = new this();
            }

            return instances[`${this.name}:${areaId}`];
        }
    
    }

    class WithRoles extends PublicJobs {

        constructor() {
            super(`jobs/with_roles`);
        }

    }

    return {
        PublicJobs ,
        OwnJobs,
        ByArea,
        WithRoles,
    };

};

module.exports = [
    "CollectionService",
    factory
];
