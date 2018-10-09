"use strict";

/**
 * My messages controller
 *
 * @memberof Postulant
 * @ngdoc controller
 * @name PostulatMessagesCtl
 */

const factory = function ($q, $scope, $state, $stateParams, Messages, MModal){
                                                           

    const messages = Messages.getCollection();

    $scope.actualPage = $stateParams.page || 1;
    $scope.filterStatus = $stateParams.status || null;

    $scope.availableStatus = [
        {value: 0x00, name: "Enviados"},
        {value: 0x10, name: "Recibidos"},
        //{value: 0x20, name: "Rechazados"},
    ];

    $scope.messages = null;

    $scope.view = function (id) {
        messages.getItem(id)
            .then((postulation) => {
                MModal.open(postulation);
            });
    };

    $scope.setFilterStatus = function (status) {
        $scope.filterStatus = status;
        //$scope.updatePostulations();
    };

    $scope.changePage = function (page) {

        if (!$scope.messages || !$scope.messages.length) {
            return;
        }

        return $state.go("^.messages", {
            page: page,
            status: $scope.filterStatus
        });

    };

    $scope.updatePostulations = () => {

        var params = {
            status: $scope.filterStatus 
        };
        /*
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
            });*/

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
    "PostulantMessagesService",
    "PostulantMessageModal",
    factory
];
