"use strict";

/**
 * Postulant controller
 * @memberof Employer 
 * @ngname controller
 * @name EmployerCtl
 * @param {service} $scope
 */

const employerCtl = function ($scope) {
    $scope.data = {};
    console.log("Employer"); 
};

module.exports = [
    "$scope",
    employerCtl
];
