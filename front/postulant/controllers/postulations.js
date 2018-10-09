"use strict";

/**
 * My postulations controller
 *
 * @memberof Postulant
 * @ngdoc controller
 * @name PostulatPostulationsCtl
 */

const factory = function ($q, $scope, $state, $stateParams, Postulations,
                                                                PModal) {

    const postulations = Postulations.getCollection();

    $scope.actualPage = $stateParams.page || 1;
    $scope.filterStatus = $stateParams.status || null;

    $scope.availableStatus = [
        {value: 0x00, name: "Nuevos"},
        {value: 0x10, name: "Aceptados"},
        {value: 0x20, name: "Rechazados"},
    ];

    $scope.postulations = null;

    $scope.view = function (id) {
        postulations.getItem(id)
            .then((postulation) => {
                PModal.open(postulation);
            });
    };

    $scope.setFilterStatus = function (status) {
        $scope.filterStatus = status;
        $scope.updatePostulations();
    };

    $scope.changePage = function (page) {

        if (!$scope.postulations || !$scope.postulations.length) {
            return;
        }

        return $state.go("^.postulations", {
            page: page,
            status: $scope.filterStatus
        });

    };

    $scope.updatePostulations = () => {

        var params = {
            status: $scope.filterStatus 
        };
        
        postulations.fetch($scope.actualPage, {params})
            .then((result) => {
                $scope.postulations = result;
            })
            .catch((res) => {
                if (res.status === 404) {
                    if ($scope.actualPage !== 1) {
                        return $scope.changePage(1);
                    }
                }
            });

    };

    return $q.all([
        $scope.updatePostulations(),
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "PostulantPostulationsService",
    "PostulantPostulationModal",
    factory
];
