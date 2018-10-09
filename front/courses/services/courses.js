"use strict";

/**
 * Courses service
 * @memberof Courses
 * @ngdoc service
 * @name CoursesService
 */
const coursesService = function ($q,Apiv1Service) {

    const COURSE_STATUS_HAB = 1;
    const COURSE_STATUS_DRAFT = 99;
    
    const get = function (relpath, params = {}) {
        var path = `courses/${relpath}`;

        return Apiv1Service.getInstance().get(path, params) 
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Invalid response");
                }
            });
    };

    const post = function (relpath, data = {}, params = {}) {
        var path =  `courses/${relpath}`;
        return Apiv1Service.getInstance().post(path, data, params)
            .then((result) => {
                
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Invalid response");
                }

            });
    };

    const put = function (relpath, data = {}, params = {}) {
        var path =  `courses/${relpath}`;
        return Apiv1Service.getInstance().put(path, data, params)
            .then((result) => {
                
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Invalid response");
                }

            });
    };

    const del = function (relpath, params = {}) {
        var path =  `courses/${relpath}`;
        return Apiv1Service.getInstance().delete(path, params);
    };

    /**
     * Get employer courses 
     * @memberof CoursesService 
     * @param {object} options
     * @return {Promise} List of courses
     */
    const getOwnCourses = function (options = {}) {
        return get('own', options);
    };

    /**
     * Get employer last courses
     * @memberof CoursesService
     * @param {object} options
     * @return {Promise}
    */
    const getOwnLasts = function (options = {}) {
        return get('own/lasts', options)
            .then((response) => {
                return response.results;
            });
    };
 
    /**
     * Get a job by pk
     * @memberof CoursesService
     * @param {object}
     * @return {Promise}
     */
    const getOwnOne = function (pk) {
        pk = parseInt(pk);
        return get(`own/${pk}/`);
    };

    /**
     * Add new Course
     * @memberof CoursesService
     * @param {object} data 
     * @return {Promise}
     */
    const saveCourse = function (data, status = COURSE_STATUS_HAB) {       
        data.status = status;

        if (data.pk) {
            data.pk = parseInt(data.pk);
            return put(`own/${data.pk}/`, data);
        } else {
            return post("own", data);
        }
       
       
    };

    const saveDraft = function (data) {
        this.saveCourse(data, COURSE_STATUS_DRAFT);
    };

    const delCourses = function (id) {
        id = parseInt(id);
        return del(`own/${id}/`);
    };

    /**
     * Get own courses info 
     * @return {Promise}
     */
    const getOwnCoursesInfo = function () {
        return get("own_info");
    };

    /**
     * Get availables hierachies
     * @memberof TechsService
     * @return {Promise}
     */
    const getAvailableHierarchies = function () {
        return get(`hierarchies`);
    };

    return {
        getOwnOne,        
        getOwnCourses,
        getOwnLasts,
        saveDraft,
        saveCourse,
        delCourses,
        getOwnCoursesInfo,
        getAvailableHierarchies
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    coursesService
];
