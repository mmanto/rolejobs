"use strict";

const angular = require("angular");

/**
 * Controller for emplouer signup
 * @memberof Employer
 * @ngdoc controller 
 * @name EmployerSignupCtl
 * @param {service} $rootScope
 * @param {service} $scope
 * @param {service} $state
 * @param {service} $modal
 * @param {Employer.EmployerService} EmployerService
 */
const SignupController = function ($rootScope, $scope, $state, $modal,
                                                  FormHelper, EmployerService) {
 
    var $errorModal;

    var csh = $rootScope.$on('$stateChangeStart', (ev, toState, toParams) => {

        if ($scope.employerSignupForm.$dirty) {
            ev.preventDefault(); 
            if (window.confirm(
                "No se ha terminado de registrar, seguro que desea salir?")) {
                csh();
                $state.go(toState, toParams);
            }
        } else {
            csh();
        }

    });

    /**
     * Form data 
     * @memberof EmployerSignupCtl
     * @type object 
     */
    $scope.employerSignupData = {};
    $scope.employerGeoData = null;

    const apiErrors = new FormHelper.ApiErrorsMannager($scope);

    apiErrors.addWatcher("employerSignup");

    /**
     * Show error
     * @memberof EmployerSignupCtl
     */
    $scope.showError = function (form, data) {

        apiErrors.displayErrors(form, data);

        $errorModal = $modal.open({
            scope: $scope,
            template: "<h3>Verifique el formulario</h3>" +
                "<p>Tiene uno o mas datos inválido, verifique" +
                " y vuelva a intentar</p>" + 
                `<button class="button" ng-click="dismiss()">Volver</button>`,
        });

    };

    /**
     * Close error modal
     * @memberof EmployerSignupCtl
     */
    $scope.dismiss = function() {
        if ($errorModal) {
            $errorModal.dismiss();
        }
    };

    /**
     * Signup form submit
     * @memberof EmployerSignupCtl
     */
    $scope.signup = function (form) {

        FormHelper.isValid(form)
            .then(() => {
                let data = angular.copy($scope.employerSignupData);

                if ($scope.employerGeoData) {
                    let geo = $scope.employerGeoData;
                    data.address = geo.address;
                    data.country = geo.country;
                    data.region = geo.region;
                    data.city = geo.city;
                }

                return EmployerService.signup(data);

            })
            .then(() => {
                csh(); 

                $state.go("accounts.confirmationsent", {
                    email: $scope.employerSignupData.email
                });

            })
            .catch((response) => {
                if (response.data) {
                    $scope.showError(form, response.data);
                }
            });
    };

};

module.exports = [
    "$rootScope",
    "$scope",
    "$state",
    "$modal",
    "FormHelper",
    "EmployerService",
    SignupController
];
