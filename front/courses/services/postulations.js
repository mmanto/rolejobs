"use strict";

/**
 * @memberof Courses
 * @ngdoc service
 * @name PostulationsCoursesService
 */

const factory = function (CollectionService) {

    class OwnCoursePostulationsRecordSet extends
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

    class OwnCoursePostulations extends CollectionService.Collection {

        constructor(courseId) {
            jobId = parseInt(jobId);
            super(`course/own/${jobId}/postulations`);
            this._courseId = courseId;
        }

        _getRecordSetClass() {
            return OwnCoursePostulationsRecordSet;
        }
    
    }

    return {
        OwnCoursePostulations
    };

};

module.exports = [
    "CollectionService",
    factory
];
