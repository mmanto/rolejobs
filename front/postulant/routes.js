"use strict";

const postulantTemplate = require('postulant/postulant.html');
const cvTemplate = require("postulant/cv.html");
const myPostulationsTemplate = require("postulant/my_postulations.html");
const myMessagesTemplate = require("postulant/my_messages.html");
const myFavoritesTemplate = require("postulant/my_favorites.html");
module.exports = ["$stateProvider", ($stateProvider) => {

    $stateProvider
        .state("postulant", {
            url: "/postulant",
            abstract: true,
            template: postulantTemplate,
            controller: "PostulantCtl",
            resolve: {
                loggedUser: ['AccountService', (AccountService) => {
                    return AccountService.getLoggedUser();
                }]
            }
        })

        .state('postulant.home', {
            url:"/home",
            data: {
                tab: "home"
            },
            views: {
                "postulant-main": {
                    template: '<h1>Home</h1>',
                    controller: "PostulantHomeCtl"
                }
            }
        })

        .state('postulant.postulations', {
            url:"/postulations/{page: int}",
            params: {
                page: null,
                status: null,
            },
            data: {
                tab: "postulations"
            },
            views: {
                "postulant-main": {
                    template: myPostulationsTemplate,
                    controller: "PostulatPostulationsCtl"
                }
            }
        })

        .state('postulant.cv', {
            url:"/cv",
            data: {
                tab: "cv"
            },
            views: {
                "postulant-main": {
                    template: cvTemplate,
                    controller: "PostulantCvCtl"
                }
            }
        })
        /*Courses*/
        .state('postulant.courses', {
            url:"/courses/",
            params: {
                page: null,
                status: null,
            },
            data: {
                tab: "courses"
            },
            views: {
                "postulant-main": {
                    template: myPostulationsTemplate,
                    controller: "PostulatPostulationsCtl"
                }
            }
        })
        
        /*Message*/
        .state('postulant.messages', {
//            url:"/messages/{page: int}",
            url:"/messages/",
            params: {
                page: null,
                status: null,
            },
            data: {
                tab: "messages"
            },
            views: {
                "postulant-main": {
                    template: myMessagesTemplate,
                    controller: "PostulatMessagesCtl"
                }
            }
        })

        .state('postulant.favorites', {
            url:"/favorites/",
            params: {
                page: null,
                status: null,
            },
            data: {
                tab: "favorites"
            },
            views: {
                "postulant-main": {
                    template: myFavoritesTemplate,
                    controller: "PostulatFavoritesCtl"
                }
            }
        })
    ;
}];
