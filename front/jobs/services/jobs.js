"use strict";

/**
 * Jobs service
 * @memberof Jobs
 * @ngdoc service
 * @name JobsService
 */
const jobsService = function ($q, Apiv1Service) {

    const JOB_STATUS_HAB = 1;
    const JOB_STATUS_DRAFT = 99;
    const LANGUAGE_REQUIREMENTS = "language_requirements";
    const KNOWLEDGE_REQUIREMENTS = "knowledge_requirements";

    const get = function (relpath, params = {}) {
        var path = `jobs/${relpath}`;

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
        var path =  `jobs/${relpath}`;
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
        var path =  `jobs/${relpath}`;
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
        var path =  `jobs/${relpath}`;
        return Apiv1Service.getInstance().delete(path, params);
    };

    /**
     * Get employer jobs 
     * @memberof JobsService 
     * @param {object} options
     * @return {Promise} List of jobs
     */
    const getOwnJobs = function (options = {}) {
        return get('own', options);
    };

    /**
     * Get employer last jobs
     * @memberof JobsService
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
     * @memberof JobsService
     * @param {object}
     * @return {Promise}
     */
    const getOwnOne = function (pk) {
        pk = parseInt(pk);
        return get(`own/${pk}/`);
    };

    /**
     * Add new Job
     * @memberof JobsService
     * @param {object} data 
     * @return {Promise}
     */
    const saveJob = function (data, status = JOB_STATUS_HAB) {
        data.status = status;

        data.requirements = data.requirements.map((r) => {
            if (r.id <= 0) {
                delete r.id;
            }

            return r;
        });

        data[LANGUAGE_REQUIREMENTS] = data[LANGUAGE_REQUIREMENTS].map((r) => {
            if (r.id <= 0) {
                delete r.id;
            }

            return r;
        });

        data[KNOWLEDGE_REQUIREMENTS] = data[KNOWLEDGE_REQUIREMENTS].map((r) => {
            if (r.id <= 0) {
                delete r.id;
            }

            return r;
        });

        data.questions = data.questions.map((q) => {
            if (q.id <= 0) {
                delete q.id;
            }

            if (q.options && q.options.length) {
                q.options = q.options.map((o) => {
                    if (o.id <= 0) {
                        delete o.id;
                    }
                    return o;
                });
            }

            return q;
        });

        if (data.pk) {
            data.pk = parseInt(data.pk);
            return put(`own/${data.pk}/`, data);
        } else {
            return post("own", data);
        }

    };

    /**
     * Add new Job
     * @memberof JobsService
     * @param {object} data 
     * @return {Promise}
     */
    const saveDraft = function (data) {
        this.saveJob(data, JOB_STATUS_DRAFT);
    };

    const delJob = function (id) {
        id = parseInt(id);
        return del(`own/${id}/`);
    };

    /**
     * Get own jobs info 
     * @return {Promise}
     */
    const getOwnJobsInfo = function () {
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
        getOwnJobs,
        getOwnLasts,
        saveJob,
        saveDraft,
        delJob,
        getOwnJobsInfo,
        getAvailableHierarchies
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    jobsService
];
