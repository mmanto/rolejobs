"use strict";

/**
 * Job postulation controller
 * @memberof Employer
 * @ngdoc controller
 * @name EmployerJobPostulationCtl
 */

const factory = function ($q, $scope, $params, alert, JobsCollections,
    PostulationsService) {

    const EDUCATION_REQUIREMENT = "education_requirement";
    const EDUCATION_LEVEL = "education_level";
    const EDUCATION_FINISH_LEVEL = "education_finish_level";
    const LANGUAGE_REQUIREMENTS = "language_requirements";
    const QUESTION_ID = "question_id";

    const jobPk = $params.jobPk;
    const postulantPk = $params.pk;
    const jobs = JobsCollections.OwnJobs.getInstance();
    const postulations = new PostulationsService.OwnJobPostulations(jobPk);

    $scope.job = {};
    $scope.postulation = {};

    $scope.requirements = {
        education: null,
        languages: [],
    };

    $scope.setStatus = function (status) {
        if ($scope.postulation) {
            $scope.postulation.$setStatus(status)
                .then(() => {
                    $scope.updatePostulation();
                })
                .catch(() => {
                    alert.open("Hubo un error al cambiar el estado");
                });
        }
    };

    $scope.updateJob = function () {
        return jobs.getItem(jobPk)
            .then((job) => {
                $scope.job = job;
            });
    };

    $scope.updatePostulation = function () {
        return postulations.getItem(postulantPk)
            .then((postulation) => {
                $scope.postulation = postulation;
            });
    };

    $scope.resolveRequirements = function () {

        // Education requirement:
        var educationReuirement = $scope.job[EDUCATION_REQUIREMENT];
        if (educationReuirement && educationReuirement.level) {

            var educationLevel = educationReuirement.finished ?
                ($scope.postulation.user[EDUCATION_FINISH_LEVEL] || 0) :
                ($scope.postulation.user[EDUCATION_LEVEL] || 0);


            if (educationLevel & educationReuirement.level) {
                $scope.requirements.education = {
                    level: "success",
                    msg: "El nivel de educación es el requerido"
                };
            } else {
                $scope.requirements.education = {
                    level: educationReuirement.exclusive ?
                        "alert" : "warning",
                    msg: "El nivel de educación no es el requerido"
                };
            }
        }

        // Languages
        var languagesRequirements = $scope.job[LANGUAGE_REQUIREMENTS];
        var userLanguages = $scope.postulation.user.languages;

        if (languagesRequirements && languagesRequirements.length) {

            $scope.requirements.languages = languagesRequirements
                .map((reqlang) => {
                    var userLang = userLanguages
                        .find(l => l.id === reqlang.language);

                    if (!userLang) {
                        return {
                            language: reqlang,
                            msg: "No tiene este idioma cargado",
                            type: reqlang.exclusive ? "alert" : "warning"
                        };
                    }

                    if (reqlang.level > userLang.level) {
                        return {
                            language: reqlang,
                            msg: "No tiene el nivel requerido",
                            type: reqlang.exclusive ? "alert" : "warning"
                        };
                    } else {
                        return {
                            language: reqlang,
                            msg: "Requisito cumplido",
                            type: "success"
                        };
                    }

                });
        
        }

    };

    $scope.getAnswer = function (questionId) {
        return $scope.postulation.questionsanswers
            .find(i => i[QUESTION_ID] === questionId);
    };

    return $q.all([
        $scope.updateJob(),
        $scope.updatePostulation()
    ]).then(() => {
        return $scope.resolveRequirements();
    });

};

module.exports = [
    "$q",
    "$scope",
    "$stateParams",
    "AlertModal",
    "JobsCollections",
    "PostulationsService",
    factory
];
