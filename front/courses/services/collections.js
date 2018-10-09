"use strict";

/**
 * Courses collection
 * @memberof Courses
 * @ngdoc service
 * @name CoursesCollections
 */

const factory = function (CollectionService) {

    var instances = {};

    class PublicCourseRecordSet extends CollectionService.CollectionRecordSet {
        
        _extendItem(item) {
            item = super._extendItem(item);
            item.$postulate = (data) => {
                var path = `${item.id}/postulate`;
                return this.collection.post(data, {}, path)
                    .then((result) => {
                        console.log("RESULT", result);
                    });
            };
            return item;
        }

    }

    class CoursesCollectionBase extends CollectionService.Collection {

        constructor(path) {
            if (typeof instances[path] !== "undefined") {
                throw new Error("Use getInstance");
            }

            super(`courses/${path}`);
        }

        static getInstance() {
            if (typeof instances[this.name] === "undefined") {
                instances[this.name] = new this();
            }

            return instances[this.name];
        }

    } 

    class PublicCourses extends CoursesCollectionBase {

        constructor(path = "courses") {
            super(path);
        }

        _getRecordSetClass() {
            return PublicCourseRecordSet;
        }

    }

    class OwnCourses extends CoursesCollectionBase {

        constructor() {
            super("own");
        }

    }


    return {
        PublicCourses ,
        OwnCourses
    };

};

module.exports = [
    "CollectionService",
    factory
];
