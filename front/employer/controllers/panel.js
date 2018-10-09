"use strict";

const angular = require("angular");

/**
 * Employer panel controller
 * @memberof Employer 
 * @ngdoc controller
 * @name EmployerPanelCtl
 */

const factory = function ($scope, $alert, EmployerService, CroppterModal,
    AvatarsService, FormHelper) {

    $scope.employerData = {};
    $scope.employerGeoData = null;

    const apiForm = new FormHelper.ApiErrorsMannager($scope);

    apiForm.addWatcher("employer");

    $scope.save = function (form) {

        return FormHelper.isValid(form)
            .then(() => {
                let data = angular.copy($scope.employerData);

                if ($scope.employerGeoData) {
                    let geo = $scope.employerGeoData;
                    data.address = geo.address;
                    data.country = geo.country;
                    data.region = geo.region;
                    data.city = geo.city;
                }

                return EmployerService.saveMe(data);
            
            })
            .then(() => {
                $alert.open("Sus datos se han guardado correctamente");
            })
            .catch((response) => {

                if (response.required) {
                     $alert.open("Hay un error en alguno de los datos, " + 
                                " verifique y reintente");
                } else if (response.data) {
                    apiForm.displayErrors(form, response.data);
                    $alert.open("Hay un error en alguno de los datos, " + 
                                " verifique y reintente");
                } else {
                    $alert.open("Error desconocido, reintente");
                }
            });

    };

    $scope.changeProfileAvatar = function () {

        var modal = CroppterModal.open({
            width: 170,
            height: 170
        });
            
        return modal.result.then((avatar) => {
            return AvatarsService.uploadProfile(avatar.src);
        });

    };

    $scope.changeBrandAvatar = function () {

        var modal = CroppterModal.open({
            width: 400,
            height: 150
        });
            
        return modal.result.then((avatar) => {
            return AvatarsService.uploadProfile(
                "brand",
                avatar.src);
        });

    };

    return EmployerService.getMe()
        .then((data) => {

            if (data.address && data.region || data.city) {
                $scope.employerGeoData = {
                    address: data.address,
                    country: data.country,
                    region: data.region,
                    city: data.city
                };
            } else {
                $scope.employerGeoData = null;
            }

            delete data.address;
            delete data.country;
            delete data.region;
            delete data.city;

            if (data.gender) {
                data.gender = data.gender.toString();
            }

            $scope.employerData = data;
        });

};

module.exports = [
    "$scope",
    "AlertModal",
    "EmployerService",
    "CroppterModal",
    "AvatarsService",
    "FormHelper",
    factory
];
