"use strict";

/**
 * Employer courses controller
 * @ngdoc controller
 * @memberof Employer 
 * @name EmployerCoursesCtl
 */

const employerCoursesController = function ($scope, $state, $stateParams,$filter, ConfirmModal, CoursesService, CoursesCollections ) {

    const SUBAREA_TEXT = "subarea_text";

    const ownCourses = CoursesCollections.OwnCourses.getInstance();

    const dateFilter = $filter("date");

    $scope.courses = null;
    $scope.info = null;
    $scope.filterStatus = $stateParams.status || null;
    $scope.actualPage = $stateParams.page || 1;

    $scope.coursesSchema = {
        $trackBy: 'pk',
        $orderBy: "published",
        $actions: {
            "Editar" (item) {
                $scope.editCourse(item.pk); 
            },
            "Borrar" (item) {
                $scope.delCourse(item.pk);
            }
        },

        title: {
            title: "Titulo"
        },
        description: {
            title: "Descripcion"
        },
        price: {
            title: "Precio"
        },
        currency_type: {
            title: "Tipo de moneda"
        },
        course_type: {
            title: "Tipo de curso"
        }

    };

    $scope.selected = {
        items: []
    };

    $scope.editCourse = function (pk) {
        $state.go("employer.main.courseedit", {pk}); 
    };

    $scope.gotoCourse = function (pk) {
        $state.go("employer.main.course", {pk}); 
    };

    $scope.delCourse = function (pk) {
        ConfirmModal.open(
            "¿Está realmente seguro?"
        ).then(() => {
            CoursesService.delCourse(pk)
                .then(() => {
                    $scope.updateCourses();
                });
        });
    };

    $scope.changePage = function (page) {

        if (!$scope.courses) {
            return;
        }

        return $state.go("^.courses", {
            page: page,
            status: $scope.filterStatus
        });
    };

    $scope.updateCourses = function () {

        var params = {
            status: $scope.filterStatus 
        };
        
        ownCourses.fetch($scope.actualPage, {params})
            .then((rs) => {
                $scope.courses = rs;
                $scope.selected.items = [];
            })
            .catch((res) => {
                if (res.status === 404) {
                    if ($scope.actualPage !== 1) {
                        return $state.go("^.courses", {
                            page: 1,
                            status: params.status 
                        });
                    }
                }
            });

    };

    $scope.setFilterStatus = function (status) {
        $scope.filterStatus = status;
        $scope.updateCourses();
    };

    CoursesService.getOwnCoursesInfo()
        .then((info) => {
            $scope.info = info;
        });

    return $scope.updateCourses();

};

module.exports = [
    "$scope",
    "$state",
    "$stateParams",
    "$filter",
    "ConfirmModal",
    "CoursesService",
    "CoursesCollections",
    employerCoursesController
];
