"use strict";

const angular = require("angular");

const factory = function ($scope, FormHelper, jobData) {

    $scope.postulateData = {};

    const apiErrors = new FormHelper.ApiErrorsMannager($scope);
    apiErrors.addWatcher("postulate");
    
    $scope.job = jobData;
    
    $scope.formUrl = `/api/v1/jobs/jobs/${jobData.pk}/postulate_form.html`;

    $scope.postulate = function (form) {
        FormHelper.isValid(form)
            .then(() => {
                var data = {
                    answers: {} 
                };
               
                angular.forEach($scope.postulateData, (v, i) => {
                    if (i.match(/^question_[\d]+$/)) {
                        data.answers[i] = v;
                    } else {
                        data[i] = v;
                    }
                });

                console.log("Data", data);
                
                jobData.$postulate(data)
                    .then((result) => {
                        console.log(__filename, result);
                    });

            });
    };

};

module.exports = [
    "$scope",
    "FormHelper",
    "jobData",
    factory
];
