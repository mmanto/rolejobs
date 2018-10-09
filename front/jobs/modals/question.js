"use strict";

/**
 * Modal for new job question 
 * @memberof Jobs
 * @ngdoc service
 * @name QuestionModal 
 */

const angular = require("angular");

const getFakeId = (function () {
    var last = 0;

    return function () {
        return --last;
    };

})();

const factory = function ($modal) {

    const IS_REQUIRED = "is_required";
    const IS_CORRECT = "is_correct";
    const QUESTION_TYPE = "question_type";

    const modalCtl = [
        "$q",
        "$scope",
        "question",
        "options",
    function ($q, $scope, question) {

        $scope.questionData = {
            options: []
        };
        $scope.optionData = {};

        $scope.optionsSchema = {
            $trackBy: "id",
            $actions: {
                "Borrar" (item) {
                    $scope.questionData.options = $scope.questionData.options
                        .filter((i) => {
                            return i.id !== item.id;
                        });
                },
                "Es la correcta" (item) {
                    $scope.makeOptionCorrect(item.id);
                }
            },
            text: "Respuesta",
            "is_correct": {
                title: "Es la correcta",
                align: "center",
                width: "130px",
                parser(value) {
                    return value ? "Si" : "No";
                }
            }
        };

        $scope.apiErrors = {
            questionForm: {}
        };

        $scope.$watchCollection("questionData", () => {
            $scope.apiErrors.questionForm = {};    
        });

        $scope.$watchCollection("questionData.options", () => {
            $scope.apiErrors.questionForm = {};    
        });

        $scope.makeOptionCorrect = function (id) {
            $scope.questionData.options = $scope.questionData.options
                .map((q) => {
                    q[IS_CORRECT] = q.id === id;
                    return q;
                });
            $scope.$broadcast("rjtablecollection:forceupdate");
        };

        $scope.addOption = function () {

            var item = {
                id: getFakeId(),
                text: $scope.optionData.text
            };
           
            $scope.questionData.options.push(item);

            if ($scope.optionData[IS_CORRECT]) {
                $scope.makeOptionCorrect(item.id);
            }

            $scope.optionData = {
                text: "",
                "is_correct": false
            };

        };

        $scope.dirtForm = function (form) {
            if (form.$error && form.$error.required) {
                form.$error.required.forEach((f) => {
                    f.$setDirty(); 
                });
            }

            return form;
        };

        $scope.displayError = function (form, data) {
            for (var i in data) {
                if (form[i]) {
                    form[i].$setDirty();
                    // form.$setValidity(i, false);
                    $scope.apiErrors[form.$name][i] = {
                        msg: data[i][0]
                    };
                } else if (i === "$nonfield") {
                    $scope.apiErrors[form.$name][i] = {
                        msg: data[i][0]
                    };
                }

            }
        };

        $scope.save = function (form) {
            var data, correct;

            $scope.dirtForm(form);

            if (form.$invalid) {
                return;
            }

            data = angular.copy($scope.questionData);

            data[IS_REQUIRED] = !!data[IS_REQUIRED];

            if (!data.id) {
                data.id = getFakeId();
            }

            if (parseInt(data[QUESTION_TYPE]) === 48) {

                if (!data.options.length) {
                    return $scope.displayError(form, {
                        "$nonfield": ["No se definieron opciones"] 
                    });
                }

                correct = data.options.find(x => !!x[IS_CORRECT]);

                if (!correct) {
                    return $scope.displayError(form, {
                        "$nonfield": ["Debe haber una opción correcta"] 
                    });
                }

            } else {
                data.options = [];
            }

            console.log("question", data);

            $scope.$close(data);
            
        };
        
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

        $scope.loadQuestion = function () {

            if (question) {
                $scope.questionData = question;

                angular.forEach($scope.questionData, (v, k) => {
                    if (typeof v === "number") {
                        $scope.questionData[k] = v.toString();
                    } 
                });

            }

            return $q.resolve($scope.questionData);
            
        };

        return $q.all(
            $scope.loadQuestion()
        );

    }];

    const open = function (data = null, options = {}) {

        var modal = $modal.open({
            templateUrl: 
                '/api/v1/jobs/templates/new_question.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                question() {
                    return data;
                },
                options() {
                    return options;
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
    factory 
];
