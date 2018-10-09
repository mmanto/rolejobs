"use strict";

/**
 * Employer messages controller
 * @ngdoc controller
 * @memberof Employer 
 * @name EmployerMessagesCtl
 */

const employerMessagesController = function ($scope, $state, $stateParams,
                $filter, ConfirmModal) {

    const SUBAREA_TEXT = "subarea_text";

//    const ownMessages = MessagesCollections.OwnMessages.getInstance();

    const dateFilter = $filter("date");

    $scope.messages = null;
    $scope.info = null;
    $scope.filterStatus = $stateParams.status || null;
    $scope.actualPage = $stateParams.page || 1;

    $scope.messagesSchema = {
        $trackBy: 'pk',
//        $actions: {
//            "Editar" (item) {
//                $scope.editMessage(item.pk); 
//            },
//            "Borrar" (item) {
//                $scope.delMessage(item.pk);
//            }
//        },

        title: {
            title: "Titulo"
        },
//        published: {
//            title: "Publicado" ,
//            align: "center",
//            sortable: true,
//            parser (v) {
//                return dateFilter(v, "d-M-yyyy");
//            }
//        },
//        "postulants_number": {
//            title: "Postulantes",
//            align: "center",
//        },
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

    $scope.editMessage = function (pk) {
        $state.go("employer.main.messageedit", {pk}); 
    };

    $scope.gotoMessage = function (pk) {
        $state.go("employer.main.message", {pk}); 
    };

    $scope.delMessage = function (pk) {
        ConfirmModal.open(
            "¿Está realmente seguro?"
        ).then(() => {
//            MessagesService.delMessage(pk)
//                .then(() => {
//                    $scope.updateMessages();
//                });
        });
    };

    $scope.changePage = function (page) {

        if (!$scope.messages) {
            return;
        }

        return $state.go("^.messages", {
            page: page,
            status: $scope.filterStatus
        });
    };

    $scope.updateMessages = function () {

        var params = {
            status: $scope.filterStatus 
        };

//        ownMessages.fetch($scope.actualPage, {params})
//            .then((rs) => {
//                $scope.messages = rs;
//                $scope.selected.items = [];
//            })
//            .catch((res) => {
//                if (res.status === 404) {
//                    if ($scope.actualPage !== 1) {
//                        return $state.go("^.messages", {
//                            page: 1,
//                            status: params.status 
//                        });
//                    }
//                }
//            });

    };

    $scope.setFilterStatus = function (status) {
        $scope.filterStatus = status;
        $scope.updateMessages();
    };

//    MessagesService.getOwnMessagesInfo()
//        .then((info) => {
//            $scope.info = info;
//        });

    return $scope.updateMessages();

};

module.exports = [
    "$scope",
    "$state",
    "$stateParams",
    "$filter",
    "ConfirmModal",
//    "MessagesService",
//    "MessagesCollections",
    employerMessagesController
];
