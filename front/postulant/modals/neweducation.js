"use strict";

/**
 * Modal for new education
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewEducationModal
 */

const angular = require("angular");

const postulantNewEducationModalFactory = function ($modal, ConfirmModal,
                PostulantService, EducationService, CertificationModal) {

    const IS_CURRENT = 'is_current';
    const END_DATE = 'end_date';
    const NON_FIELD_ERRORS = 'non_field_errors';
    const INSTITUTION_ID = 'institution_id';

    const getTmpId = (function () {
        var last = -1;

        return function () {
            return --last;
        };
    
    })();

    const modalCtl = [
        "$scope",
        "education",
    function ($scope, education) {

        $scope.educationData = {
            certifications: []
        };

        $scope.lastEndDate = null;

        $scope.catificationsTableSchema = {
            $trackBy: 'id',

            "type_text": {
                title: "Tipo",
            },
            name: {
                title: "Nombre",

            }
        };

        $scope.selecteds = {
            certifications: []
        };

        $scope.apiErrors = {
            educationForm: {}
        };

        $scope.$watchCollection("educationData", () => {
            $scope.apiErrors.educationForm = {};    
        });

        $scope.$watch('educationData.institution', () => {
            $scope.educationData[INSTITUTION_ID] = null;
        });

        $scope.$watch('educationData.end_date', () => {
            if ($scope.educationData[END_DATE]) {
                $scope.lastEndDate = $scope.educationData[END_DATE];
                $scope.educationData[IS_CURRENT] = false;
            }
        });

        $scope.$watch('educationData.is_current', () => {
            if ($scope.educationData[IS_CURRENT]) {
                $scope.lastEndDate = $scope.educationData[END_DATE];
                $scope.educationData[END_DATE] = null;
            } else {
                if ($scope.lastEndDate) {
                    $scope.educationData[END_DATE] = $scope.lastEndDate; 
                }
            }
        });

        $scope.searchInstitution = function (val) {
            return EducationService.searchInstitution(val);
        };

        $scope.dirtForm = function (form) {
            if (form.$error && form.$error.required) {
                form.$error.required.forEach((f) => {
                    f.$setDirty(); 
                });
            }

            return form;
        };

        $scope.displayApiErrors = function (form, data) {

            if (data[NON_FIELD_ERRORS]) {
                $scope.apiErrors[form.$name].$nonfield = {
                    msg: data[NON_FIELD_ERRORS][0]
                };
            }

            for (var i in data) {
                if (form[i]) {
                    form[i].$setDirty();
                    // form.$setValidity(i, false);
                    $scope.apiErrors[form.$name][i] = {
                        msg: data[i][0]
                    };
                }
            }
        };

        $scope.save = function (form) {
            var data;

            $scope.dirtForm(form);

            if (form.$invalid) {
                return;
            }

            data = angular.copy($scope.educationData);

            PostulantService.getInstance().saveEducation(data)
                .then((data) => {
                    $scope.$close(data);
                })
                .catch((err) => {
                    if (err.data) {
                        $scope.displayApiErrors(form, err.data);
                    }
                }); 

        };
        
        $scope.cancel = function (form) {
            if (form.$dirty) {
                return ConfirmModal.open(
                    "Hay una experiencia laboral sin guardar, " +
                    "¿realmente desea cancelar?"
                ).then(() => {
                    $scope.$dismiss('canceled');
                });
            } else {
                $scope.$dismiss('canceled');
            } 
        };

        $scope.addCertification = function (cert = null) {
            var modal = CertificationModal.open(cert);
            modal.result.then((certification) => {
                certification.touched = true;

                if (certification.id) {
                    $scope.educationData.certifications = 
                        $scope.educationData.certifications
                        .map((i) => {
                            if (i.id === certification.id) {
                                return certification;
                            } else {
                                return i;
                            }
                        });
                } else {
                    certification.id = getTmpId();
                    $scope.educationData.certifications.push(certification);
                }

            });
        };

        $scope.deleteCertifications = function () {
            var ids = $scope.selecteds.certifications
                .map(i => i.id);

            $scope.educationData.certifications = $scope.educationData
                .certifications
                .filter(r => ids.indexOf(r.id) === -1);

        };

        if (education) {
            $scope.educationData = education;
            angular.forEach($scope.educationData, (v, k) => {
                if (typeof v === "number") {
                    $scope.educationData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (id = null) {

        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_education.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                education() {

                    if (!id) {
                        return null;
                    }

                    return PostulantService
                        .getInstance()
                        .getEducation(id);

                }
            }
        });

        return modal;

    };

    return {
        open
    };

};

module.exports = [
    "$modal",
    "ConfirmModal",
    "PostulantService",
    "EducationService",
    "PostulantNewCertificationModal",
    postulantNewEducationModalFactory
];
