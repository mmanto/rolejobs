"use strict";

const angular = require("angular");

module.exports = [
    '$q',
    '$rootScope',
    'Apiv1Service', 
    'AvatarsService',
/**
 * Service for postualnt management.
 * @ngdoc service 
 * @name PostulantService 
 * @memberof Rolejob.postulant
 * @param {service} $q
 * @param {service} $rootScope
 * @param {service} ApiService - Apiv1service 
 */
function ($q, $rootScope, ApiService, AvatarsService) {

    var instance;

    // const OWN_VIHICLE = "own_vehicle"; 
    const COUNTRY_OF_BIRTH = "country_of_birth";
    const MARITAL_STATUS = "marital_status";
    const DRIVER_LICENSE = "driver_license"; 
    const INSTITUTION_ID = "institution_id";

    const chan = $rootScope.$new(true);

    class Postulant {
   
        constructor () {
            this._details = null;
            this._id  = null;
        }

        get _api () {
            return ApiService.getInstance();
        }

        _get(path, params = {}) {
            return this._api.get(`postulant/${path}`, params)
                .then((res) => {
                    return res.data;
                });
        }

        _post(path, data, params = {}, options = {}) {
            data = ApiService.normalize(data);
            return this._api.post(`postulant/${path}`, data, params, options)
                .then((res) => {
                    return res.data;
                });

        }

        _put(path, data, params = {}) {
            data = ApiService.normalize(data);
            return this._api.put(`postulant/${path}`, data, params)
                .then((res) => {
                    return res.data;
                });
        }

        _delete(path, params = {}) {
            return this._api.delete(`postulant/${path}`, params)
                .then((res) => {
                    return res.data;
                });
        }


        _putOrPost(path, data, params = {}) {
            return this._get(path)
                .then(() => {
                    return this._put(path, data, params);
                })
                .catch((err) => {
                    if (err.status === 404) {
                        return this._post(path, data, params);
                    }

                    throw err;
                });

        }

        _cleanProfileData(data) {
            data[COUNTRY_OF_BIRTH] = `${data[COUNTRY_OF_BIRTH]}`;
            data[DRIVER_LICENSE] = `${data[DRIVER_LICENSE]}`;
            data[MARITAL_STATUS] = `${data[MARITAL_STATUS]}`;
            return data;
        }

        _parseProfileData(data) {
            return data;
        }


        signup(data) {
            return this._post('signup', data);
        }

        /**
         * Get profile data
         */
        getProfile() {
            return this._get('profile').then((data) => {
                return this._cleanProfileData(data);
            });
        }

        /**
         * Save profile data
         * @param {object} data 
         * @return {Promise}
        **/
        saveProfile(data) {
            data = angular.copy(data);
            data = this._parseProfileData(data);

            return this._putOrPost("profile", data);        
        }

        /**
         * Get Biography
         */
        getBiography() {
            return this._get('profile/biographic');
        }

        /**
         * Save biography
         * @param {object} data 
         * @return {Promise}
         */
        saveBiograpy(data) {
            return this._putOrPost("profile/biographic", data);
        }

        getExperiences() {
            return this._get('profile/experience');
        }

        getExperience(id) {
            id = parseInt(id);
            return this._get(`profile/experience/${id}`);
        }

        saveExperience(data) {
            const subpath = 'profile/experience';
            var cdata = angular.copy(data);

            if (cdata.id) { 
                cdata.id = parseInt(cdata.id);
                return this._put(`${subpath}/${data.id}`, cdata);
            } else {
                return this._post(subpath, cdata);
            }

        }

        deleteExperiences(ids) {
            return this._delete(`profile/experience`, {
                ids: ids.join(',')
            });
        }

        getEducations() {
            return this._get(`profile/education`);
        }

        getEducation(id) {
            id = parseInt(id);
            return this._get(`profile/education/${id}`);
        }

        saveEducation(data) {
            if (data.id) {
                data.id = parseInt(data.id);
                if (!data[INSTITUTION_ID]) {
                    delete data[INSTITUTION_ID];
                }
                return this._put(`profile/education/${data.id}`, data);
            } else {
                if (!data[INSTITUTION_ID]) {
                    delete data[INSTITUTION_ID];
                }
                return this._post('profile/education', data);
            }
        }

        deleteEducations(ids) {
            return this._delete(`profile/education`, {
                ids: ids.join(',')
            });
        }

        /* LANGUAJE SECTION */

        getLanguages() {
            return this._get(`profile/languages`);
        }

        getLanguage(id) {
            id = parseInt(id);
            return this._get(`profile/languages/${id}`);
        }

        saveLanguage(data) {
            var language = parseInt(data.language);
            var path = `profile/languages/${language}`;

            return this._get(path)
                .then(() => {
                    delete data.language;
                    return this._put(path, data);
                })
                .catch((res) => {
                    if (res.status === 404) {
                        return this._post(`profile/languages`, data);
                    }

                    throw res;
                });
                
        }

        deleteLanguages(ids) {
            return this._delete(`profile/languages`, {
                ids: ids.join(',')
            });
        }

        /* COMPUTERKNOWLEDGE SECTION */

        getComputerknowledges() {
            return this._get(`profile/computerknowledges`);
        }

        getComputerknowledge(id) {
            id = parseInt(id);
            return this._get(`profile/computerknowledges/${id}`);
        }

        saveComputerknowledge(data) {
            var computerknowledge = parseInt(data.computerknowledge);
            var path = `profile/computerknowledges/${computerknowledge}`;

            return this._get(path)
                .then(() => {
                    delete data.computerknowledge;
                    return this._put(path, data);
                })
                .catch((res) => {
                    if (res.status === 404) {
                        return this._post(`profile/computerknowledges`, data);
                    }

                    throw res;
                });
                
        }

        deleteComputerknowledges(ids) {
            return this._delete(`profile/computerknowledges`, {
                ids: ids.join(',')
            });
        }

        changeAvatar(data) {
            return AvatarsService.uploadProfile(data);
        }

        getRoles() {
            return this._get(`profile/roles`);
        }

        saveRoles(data) {
            var pks = data.map((i) => {
                return parseInt(i);
            });
            return this._post(`profile/roles`, pks);
        }

        getCompletedProfileInfo() {
            return this._get(`profile/completed`);
        }

        static getInstance() {
            if (!instance) {
                instance = new Postulant();
            }

            return instance;
        }

        static on(eventName, listener) {
            return chan.$on(eventName, listener);
        }

    }

    return Postulant; 

}];
