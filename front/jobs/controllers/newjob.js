"use strict";

/**
 * New Job modal controller
 * @memberof Jobs
 * @ngdoc controller
 * @name NewJobCtl
 */

const angular = require("angular");
const cancelModalTemplate = require("jobs/job_cancel.html");

const getFakeId = (function () {
    var last = 0;

    return function () {
        last--;
        return last;
    };

})();

const factory = function (
                            $q, 
                            $scope, 
                            $state, 
                            $stateParams,
                            $modal, 
                            ConfirmModal, 
                            AlertModal, 
                            JobsService, 
                            AreasService,
                            NewLanguageModal, ITTechModal, QuestionModal, EducationService, 
                            meData) {

    const LANGUAGE_REQUIREMENTS = "language_requirements";
    const EDUCATION_REQUIREMENT = "education_requirement";
    const KNOWLEDGE_REQUIREMENTS = "knowledge_requirements";
    const GRADE = "education_requirement_grade";
    const FINISHED = "education_requirement_finished";
    const EXCLUSIVE = "education_requirement_exclusive";
    const SUBTECHNOLOGY_TEXT = "subtechnology_text";
    const HIERARCHY_TEXT = "hierarchy_text";

    $scope.languages = [];
    $scope.grades = [];
    $scope.hierarchies = [];
    $scope.educationIsRequired = false;

    $scope.jobData =  {
        "title": "",
        "description": "",
        "area": null,
        "subarea": null,
        "job_type": 0,
        "reference_number": null,
        "handicapped_postulant": true,
        "show_address": false,
        "get_cvs_ctrl_panel": true,
        "send_cvs_by_mail": false,
        "requirements": [],
        "language_requirements": [],
        "education_requirement": {},
        "knowledge_requirements": [],
        "education_requirement_grade": "-1",
        "questions": [],
    };

    $scope.jobGeoData = null;

    $scope.lastJobs = [];

    $scope.requirementsSchema = {
        $trackBy: "id",
        $actions: {
            "Borrar" (item) {
                $scope.jobData.requirements = $scope.jobData.requirements
                    .filter((i) => {
                        return i.id !== item.id; 
                    });
            }
        },
        description: "Requisito",
        exclusive: {
            title: "Excluyente",
            width: "140px",
            align: "center",
            parser (val) {
                return val ? "Si" : "No";
            }
        }
    };

    $scope.languageRequirementsSchema = {
        $trackBy: "id",
        $actions: {
            "Borrar" (item) {
                $scope.jobData[LANGUAGE_REQUIREMENTS] = 
                    $scope.jobData[LANGUAGE_REQUIREMENTS]
                    .filter((i) => {
                        return i.id !== item.id; 
                    });
            }
        },
        name: "Idioma requerido",
        level: {
            title: "Nivél requerido",
            parser(data) {
                return `${data}/10`;
            }
        },
        exclusive: {
            title: "Excluyente",
            width: "140px",
            align: "center",
            parser (val) {
                return val ? "Si" : "No";
            }
        }
    };

    $scope.knowledgeRequirementsSchema = {
        $trackBy: "id",
        $actions: {
            "Borrar" (item) {
                $scope.jobData[KNOWLEDGE_REQUIREMENTS] = 
                    $scope.jobData[KNOWLEDGE_REQUIREMENTS]
                    .filter((i) => {
                        return i.id !== item.id; 
                    });
            }
        },
        "technology_text": {
            title: "Tecnología",
            parser(data, item) {
                return `${data} -> ${item[SUBTECHNOLOGY_TEXT]}`;
            }
        },
        "hierarchy_text": {
            title: "Nivél requerido",
            align: "center",
            width: "160px",
            parser(data, item) {
                if (data) {
                    return data;
                } else {
                    return $scope.hierarchies
                        .find(i => i.pk === parseInt(item.hierarchy))
                        .name;
                }
            }
        },
        exclusive: {
            title: "Excluyente",
            width: "140px",
            align: "center",
            parser (val) {
                return val ? "Si" : "No";
            }
        }
    };

    $scope.questionsSchema = {
        $trackBy: "id",
        $actions: {
            "Borrar" (item) {
                $scope.jobData.questions = $scope.jobData.questions
                    .filter((q) => {
                        return q.id !== item.id;
                    });
            },
            "Editar" (item) {
                $scope.addQuestion(item);
            }
        },
        /*"type_text": {
            title: "Tipo",
            align: "center",
            width: "160px"
        },*/
        question: "Pregunta" 
    };

    $scope.areaOptions = {
        subareas: []
    };

    $scope.isNew = true;

    $scope.pk = null;

    $scope.req = {};

    $scope.selected = {
        requirements: [],
        languageRequirements: [],
    };

    var qmodal;

    $scope.apiErrors = {
        jobForm: {}
    };

    $scope.$watch('jobData.area', (areaId) => {

        if (!areaId) {
            $scope.areaOptions.subareas = [{
                pk: "",
                name: "Seleccione un Area"
            }];
            return;
        }

        AreasService.byId(areaId)
            .then((data) => {
                $scope.areaOptions.subareas = [{
                    pk: "",
                    name: "---------"
                }].concat(data.subareas);

                // If subarea is defined by id, search the complete
                // record.
                if (typeof $scope.jobData.subarea !== "object") {
                    $scope.jobData.subarea = data.subareas.find((a) => {
                        return a.pk === parseInt($scope.jobData.subarea, 10);
                    });
                }

            });
    });

    $scope.addRequirement = function () {
        $scope.jobData.requirements.push({
            id: getFakeId(),
            description: $scope.req.description,
            exclusive: $scope.req.exclusive || false
        });
        $scope.req = {};
    };

    $scope.addLanguageRequirement = function () {
        var modal = NewLanguageModal.open(null, {
            exclusive: true,
            nosave: true
        });

        return modal.result.then((language) => {
            console.log(language);

            var langData = $scope.languages.find((l) => {
                return l.id === parseInt(language.language);
            });

            $scope.jobData[LANGUAGE_REQUIREMENTS].push({
                id: getFakeId(),
                language: langData.id,
                name: langData.name,
                level: language.level,
                exclusive: language.exclusive || false
            });

        });

    };

    $scope.addKnowledgeRequirement = function () {
        var modal = ITTechModal.open(null, {
            showExclusive: true
        });

        return modal.result.then((req) => {
            $scope.jobData[KNOWLEDGE_REQUIREMENTS].push({
                id: getFakeId(),
                technology: req.technology,
                subtechnology: req.subtechnology,
                hierarchy: req.hierarchy,
                exclusive: req.exclusive || false,
                "technology_text": req.techInfo.name,
                "subtechnology_text": req.subTechInfo.name,
            });

        });
    };

    $scope.addQuestion = function (data = null) {

        var modal = QuestionModal.open(data);

        return modal.result.then((question) => {

            var actual = $scope.jobData.questions
                .find(q => q.id === question.id);

            if (actual) {
                $scope.jobData.questions = $scope.jobData.questions
                    .map((q) => {
                        if (q.id === question.id) {
                            return question;
                        } else {
                            return q;
                        }
                    });
            } else {
                $scope.jobData.questions.push(question);
            }

        });
    
    };

    $scope.cancel = function (definitive = false) {

        if (definitive) {
            console.log("Cancel!!");

            if (qmodal) {
                qmodal.close();
            }

            $state.go("employer.main.jobs");
            return;
        }

        qmodal = $modal.open({
            template: cancelModalTemplate,
            scope: $scope,
            backdrop: true
        }); 

    };

    $scope.error = function (err) {
        console.log(":(", err);
       
        if ($scope.jobForm.$error.required) {
            $scope.jobForm.$error.required.forEach((f) => {
                f.$setDirty();
            });
        }

        if (err.status >= 500 && err.status <= 599) {
            return AlertModal.open(
                "Ha habido un problema al procesar su publicación, por " +
                "favor, reintente."
            );
        }

        if (err && err.data && typeof err.data === "object") {
            for (var i in err.data) {

                if (!i.match(/^\w/i)) {
                    continue;
                }

                $scope.apiErrors.jobForm[i] = {
                    msg: err.data[i][0]
                };
                $scope.jobForm.$setValidity(i, false);
            }

        }

        AlertModal.open(
            "Verifique los datos e intente de nuevo",
            "El formulario contiene errores"
        );

    };

    $scope.success = function (result) {
        console.log("yea", result);
        if (qmodal) {
            qmodal.close();
        }
        $state.go("employer.main.jobs");
    };

    $scope.prepareData = function () {
        var data = angular.copy($scope.jobData);
        data.subarea = $scope.jobData.subarea.pk;

        if ($scope.pk) {
            data.pk = $scope.pk;
        }

        if ($scope.educationIsRequired) {
            data[EDUCATION_REQUIREMENT] = {
                level: data[GRADE],
                finished: data[FINISHED],
                exclusive: data[EXCLUSIVE]
            };
        } else  {
            delete data[EDUCATION_REQUIREMENT];
        }

        if ($scope.jobGeoData) {
            data.address = $scope.jobGeoData.address;
            data.country = $scope.jobGeoData.country;
            data.region = $scope.jobGeoData.region;
            data.city = $scope.jobGeoData.city;
        }

        delete data[GRADE];
        delete data[FINISHED];
        delete data[EXCLUSIVE];
   
        return data;
    };

    $scope.save = function () {
        
        if ($scope.jobForm.$invalid) {
            return $scope.error();
        }

        var data = $scope.prepareData();

        JobsService.saveJob(data)
            .then($scope.success)
            .catch($scope.error);

    };

    $scope.draft = function () {

        if ($scope.jobForm.$invalid) {
            return $scope.error();
        }

        var data = $scope.prepareData();

        JobsService.saveDraft(data)
            .then($scope.success)
            .catch($scope.error);
    };

    $scope.setJob = function (job, asNew = false) {

        if (asNew) {
            $scope.isNew = true;
            delete job.id;
            delete job.pk;
        } else {
            $scope.isNew = false;
            $scope.pk = job.pk;
        }

        $scope.jobData = job;
        $scope.pk = job.pk;

        angular.forEach($scope.jobData, (v, k) => {

            if (k === "reference_number") {
                return;
            }

            if (typeof v === "number") {
                $scope.jobData[k] = v.toString();
            } 

        });

        if (typeof $scope.jobData[EDUCATION_REQUIREMENT] === "undefined" ||
            !$scope.jobData[EDUCATION_REQUIREMENT]) {
            $scope.jobData[EDUCATION_REQUIREMENT] = {};
            $scope.educationIsRequired = false;
        } else {
            $scope.educationIsRequired = true;

            angular.forEach(
                $scope.jobData[EDUCATION_REQUIREMENT], (v, k) => {

                    if (typeof v === "number") {
                        $scope.jobData[EDUCATION_REQUIREMENT][k] =
                            v.toString();
                    } 

                });

            $scope.jobData[GRADE] = $scope.jobData[
                EDUCATION_REQUIREMENT].level;

            $scope.jobData[EXCLUSIVE] = $scope.jobData[
                EDUCATION_REQUIREMENT].exclusive;

            $scope.jobData[FINISHED] = $scope.jobData[
                EDUCATION_REQUIREMENT].finished;

        }

        if (job.geo) {
            $scope.jobGeoData = {
                address: job.geo.address,
                country: job.geo.country,
                region: job.geo.region,
                city: job.geo.city,
            };

            delete job.address;
            delete job.country;
            delete job.region;
            delete job.city;

        } else {
            $scope.jobGeoData = {};
        }

        if (asNew) {
            $scope.jobData.requirements =
                $scope.jobData.requirements.map((r) => {
                    r.id = getFakeId();
                    return r;
                });
            $scope.jobData[LANGUAGE_REQUIREMENTS] = 
                $scope.jobData[LANGUAGE_REQUIREMENTS].map((i) => {
                    i.id = getFakeId();
                    return i;
                });
            $scope.jobData[KNOWLEDGE_REQUIREMENTS] = 
                $scope.jobData[KNOWLEDGE_REQUIREMENTS].map((i) => {
                    i.id = getFakeId();
                    return i;
                });
            $scope.jobData.questions =
                $scope.jobData.questions.map((q) => {
                    q.id = getFakeId();

                    q.options = q.options.map((o) => {
                        o.id = getFakeId();
                        return o;
                    });

                    return q;

                });
        }

        return job;

    };

    $scope.cloneFrom = function (jobId, form) {

        $q.when((() => {

            if (form.$dirty) {
                return ConfirmModal.open(
                    "Hay una edición en proceso, esto pisará todos los" + 
                    " campos, ¿está seguro de continuar?");
            } 

            return true;

        })()).then(() => {
            JobsService.getOwnOne(jobId)
                .then((j) => $scope.setJob(j, true));
        });

    };

    $scope.loadJob = function() {

        return $q.when($stateParams.pk !== "-1", (areJob) => {

            if (!areJob) {

                // If the job is new job, set the same geo data than employer
                if (!$scope.jobGeoData) {
                    $scope.jobGeoData = {
                        address: meData.address,
                        country: meData.country,
                        region: meData.region,
                        city: meData.city,
                    };
                }

                return null;
            }

            $scope.isNew = false;

            return JobsService.getOwnOne($stateParams.pk)
                .then($scope.setJob);
        });

    };

    $scope.updateLanguages = function () {
        EducationService.getLanguages().then((langs) => {
            $scope.languages = langs;
        });
    };

    $scope.updateGrades = function () {
        EducationService.getGrades().then((grades) => {
            $scope.grades = grades;
        });
    };

    $scope.updateHierarchies = function () {
        JobsService.getAvailableHierarchies().then((hierarchies) => {
            $scope.hierarchies = hierarchies;
        });
    };

    JobsService.getOwnLasts()
        .then((list) => {
            $scope.lastJobs = list;
        });


    return $q.all([
        $scope.updateLanguages(),
        $scope.updateGrades(),
        $scope.updateHierarchies(),
        $scope.loadJob(),
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "$modal",
    "ConfirmModal",
    "AlertModal",
    "JobsService",
    "AreasService",
    "PostulantNewLanguageModal",
    "ITTechModal",
    "QuestionModal",
    "EducationService",
    "me",
    factory
];
