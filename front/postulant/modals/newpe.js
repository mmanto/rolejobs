"use strict";

/**
 * Modal for new Professional experience
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewPEModal
 */

const angular = require("angular");

const postulantNewPEModalService = function ($modal, ConfirmModal,
                  ReferenceModal, PostulantService, AreasService) {

    const START_DATE = 'start_date';
    const IS_CURRENT = 'is_current';
    const END_DATE = 'end_date';
    const NON_FIELD_ERRORS = 'non_field_errors';

    const getTmpId = (function () {
        var last = -1;

        return function () {
            return --last;
        };
    
    })();

    const modalCtl = [
        "$scope",
        "experience",
    function ($scope, experience) {
        
        $scope.peData = {
            subarea: null,
            references: [],
        };

        $scope.referencesTableSchema = {
            $trackBy: 'id',

            "type_text": {
                title: "Tipo",
            },
            name: {
                title: "Nombre",

            },
            email: {
                title: "Correo electrónico"
            },
            phone: {
                title: "Teléfono de contacto" 
            },
        };

        $scope.selectedReferences = {
            items: []
        };

        $scope.lastEndDate = null;

        $scope.peOptions = {};

        $scope.apiErrors = {
            peForm: {}
        };

        $scope.$watchCollection("peData", () => {
            $scope.apiErrors.peForm = {};    
        });

        $scope.$watch('peData.area', (areaId) => {

            if (!areaId) {
                $scope.peOptions.subareas = [{
                    pk: "",
                    name: "Seleccione un Area"
                }];
                return;
            }

            AreasService.byId(areaId)
                .then((data) => {
                    $scope.peOptions.subareas = [{
                        pk: "",
                        name: "---------"
                    }].concat(data.subareas);

                    // If subarea is defined by id, search the complete
                    // record.
                    if (typeof $scope.peData.subarea !== "object") {
                        $scope.peData.subarea = data.subareas.find((a) => {
                            return a.pk === parseInt($scope.peData.subarea, 10);
                        });
                    }

                });
        });

        $scope.$watch('peData.end_date', () => {
            if ($scope.peData[START_DATE]) {
                $scope.startDate = $scope.peData[START_DATE];
                }               
        });

        $scope.$watch('peData.end_date', () => {
            if ($scope.peData[END_DATE]) {
                $scope.lastEndDate = $scope.peData[END_DATE];
                $scope.peData[IS_CURRENT] = false;
            }
        });

        $scope.isCurrentSet = function () {
            if ($scope.peData[IS_CURRENT]) {
                $scope.lastEndDate = $scope.peData[END_DATE];
                $scope.peData[END_DATE] = null;
            } else {
                if ($scope.lastEndDate) {
                    $scope.peData[END_DATE] = $scope.lastEndDate; 
                }
            }
        };

        $scope.addReference = function (data) {
            var modal = ReferenceModal.open(data);
            modal.result.then((reference) => {

                reference.touched = true;

                if (reference.id) {
                    $scope.peData.references = $scope.peData.references
                        .map((i) => {
                            if (i.id === reference.id) {
                                return reference;
                            } else {
                                return i;
                            }
                        });
                } else {
                    reference.id = getTmpId();
                    $scope.peData.references.push(reference);
                }

            });
        };

        $scope.deleteReferences = function () {
            var ids = $scope.selectedReferences.items
                .map(i => i.id);

            $scope.peData.references = $scope.peData.references
                .filter(r => ids.indexOf(r.id) === -1);

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

            data = angular.copy($scope.peData);

            data.subarea = $scope.peData.subarea.pk;

            data.references = data.references.map((ref) => {
                if (ref.id < 0) {
                    ref.id = null;
                }

                return ref;
            }); 

            PostulantService.getInstance().saveExperience(data)
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

        if (experience) {
            $scope.peData = experience;
            angular.forEach($scope.peData, (v, k) => {
               
                if (k === "salary") {
                    return;
                }

                if (typeof v === "number") {
                    $scope.peData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (id) {
        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_pe.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                experience() {
                    if (!id) {
                        return null;
                    }

                    return PostulantService
                        .getInstance()
                        .getExperience(id);

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
    "PostulantNewReferenceModal",
    "PostulantService",
    "AreasService",
    postulantNewPEModalService
];
