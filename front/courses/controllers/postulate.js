"use strict";

const angular = require("angular");

const factory = function ($scope, FormHelper, courseData) {

    $scope.postulateData = {};

    const apiErrors = new FormHelper.ApiErrorsMannager($scope);
    apiErrors.addWatcher("postulate");
    
    $scope.course = courseData;
    
    $scope.formUrl = `/api/v1/courses/courses/${courseData.pk}/postulate_form.html`;

    $scope.postulate = function (form) {
        FormHelper.isValid(form)
            .then(() => {
                var data = {
                    answers: {} 
                };
               
                angular.forEach($scope.postulateData, (v, i) => {
                     data[i] = v;
                });

                console.log("Data", data);
                
                courseData.$postulate(data)
                    .then((result) => {
                        console.log(__filename, result);
                    });

            });
    };

};

module.exports = [
    "$scope",
    "FormHelper",
    "courseData",
    factory
];
