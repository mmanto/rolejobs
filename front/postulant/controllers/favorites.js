"use strict";

/**
 * My messages controller
 *
 * @memberof Postulant
 * @ngdoc controller
 * @name PostulatFavoritesCtl
 */

const factory = function ($q, $scope, $state, $stateParams, PostulantFavoritesService, MModal){
                                                           

    const favoritesCollection = PostulantFavoritesService.getCollection();

    $scope.actualPage = $stateParams.page || 1;
    

    $scope.favorites = null;

    

    $scope.changePage = function (page) {

        if (!$scope.messages || !$scope.messages.length) {
            return;
        }

        return $state.go("^.favorites", {
            page: page,
        });

    };

    $scope.updateFavorites = () => {

        favoritesCollection.fetch($scope.actualPage || 1)
        .then((favorites) => {
            $scope.favorites = favorites;
        });
    };

    return $q.all([
        $scope.updateFavorites(),
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "PostulantFavoritesService",
    factory
];
