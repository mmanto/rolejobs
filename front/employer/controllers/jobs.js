"use strict";

/**
 * Employer jobs controller
 * @ngdoc controller
 * @memberof Employer 
 * @name EmployerJobsCtl
 */

const employerJobsController = function ($scope, $state, $stateParams,
                $filter, ConfirmModal, JobsService, JobsCollections ) {

    const SUBAREA_TEXT = "subarea_text";

    const ownJobs = JobsCollections.OwnJobs.getInstance();

    const dateFilter = $filter("date");

    $scope.jobs = null;
    $scope.info = null;
    $scope.filterStatus = $stateParams.status || null;
    $scope.actualPage = $stateParams.page || 1;

    $scope.jobsSchema = {
        $trackBy: 'pk',
        $orderBy: "published",
        $actions: {
            "Editar" (item) {
                $scope.editJob(item.pk); 
            },
            "Borrar" (item) {
                $scope.delJob(item.pk);
            }
        },

        title: {
            title: "Titulo"
        },
        published: {
            title: "Publicado" ,
            align: "center",
            sortable: true,
            parser (v) {
                return dateFilter(v, "d-M-yyyy");
            }
        },
        "postulants_number": {
            title: "Postulantes",
            align: "center",
        },
        "area_text": {
            title: "Area",
            align: "center",
            parser (v, $item) {
                var area = v;
                var subarea = $item[SUBAREA_TEXT];
                return `${area} -> ${subarea}`;
            }
        },
        "status_text": {
            title: "Estado",
            align: "center"
        },
    };

    $scope.selected = {
        items: []
    };

    $scope.editJob = function (pk) {
        $state.go("employer.main.jobedit", {pk}); 
    };

    $scope.gotoJob = function (pk) {
        $state.go("employer.main.job", {pk}); 
    };

    $scope.delJob = function (pk) {
        ConfirmModal.open(
            "¿Está realmente seguro?"
        ).then(() => {
            JobsService.delJob(pk)
                .then(() => {
                    $scope.updateJobs();
                });
        });
    };

    $scope.changePage = function (page) {

        if (!$scope.jobs) {
            return;
        }

        return $state.go("^.jobs", {
            page: page,
            status: $scope.filterStatus
        });
    };

    $scope.updateJobs = function () {

        var params = {
            status: $scope.filterStatus 
        };

        ownJobs.fetch($scope.actualPage, {params})
            .then((rs) => {
                $scope.jobs = rs;
                $scope.selected.items = [];
            })
            .catch((res) => {
                if (res.status === 404) {
                    if ($scope.actualPage !== 1) {
                        return $state.go("^.jobs", {
                            page: 1,
                            status: params.status 
                        });
                    }
                }
            });

    };

    $scope.setFilterStatus = function (status) {
        $scope.filterStatus = status;
        $scope.updateJobs();
    };

    JobsService.getOwnJobsInfo()
        .then((info) => {
            $scope.info = info;
        });

    return $scope.updateJobs();

};

module.exports = [
    "$scope",
    "$state",
    "$stateParams",
    "$filter",
    "ConfirmModal",
    "JobsService",
    "JobsCollections",
    employerJobsController
];
