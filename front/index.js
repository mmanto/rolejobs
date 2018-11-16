"use strict";

// To fix jquery-ui-browserify
const $ = window.$ = window.jQuery = require('jquery');
require('jquery-ui-browserify');

// Fix compatibility 
// $.event.props = [];

//require('fastclick');
require("./shims/foundation");
//require('foundation-sites-5-tabs');
require('angular-foundation');
//require('js-cookie');
require('ng-tags-input');
require("angular-ui-router");
require("angular-cookies");
require("angular-translate");
require("angular-relative-date");

const textAngular = require("textangular");
const angularSanitaze = require("angular-sanitize");

const angular = require('angular');

const homeModule = require('./home');
const accountsModule = require('./accounts');
const postulantsModule = require("./postulant");
const employerModule = require("./employer");
const apiModule = require("./apiv1");
const jobsModule = require("./jobs");
const coursesModule = require("./courses");
const educationModule = require("./education");
const avatarsModule = require("./avatars");
const filtersModule = require("./filters");
const utilsModule = require("./utils");
const geoModule = require("./geo");
const cropperModule = require("./cropper");

// const postulantBarTemplate = require("parts/barpostulant.html");
// const employerBarTemplate = require("parts/baremployer.html");
const homeTemplate = require("home/home.html");
const contactTempalte = require("home/contact.html");
const testTemplate = require("tests.html");

const relativeDateSpanish = require("angular-relative-date/translations/es");

const app = angular.module("RoleJobs", [
    "ui.router",
    "ngCookies",
    "ngMaterial",
    "mm.foundation",
    "pascalprecht.translate",
    "relativeDate",
    angularSanitaze,
    textAngular,
    homeModule.name,
    apiModule.name,
    accountsModule.name,
    postulantsModule.name,
    employerModule.name,
    jobsModule.name,
    coursesModule.name,
    educationModule.name,
    avatarsModule.name,
    filtersModule.name,
    utilsModule.name,
    geoModule.name,
    cropperModule.name,
])

    .config(($mdThemingProvider)=>{

        $mdThemingProvider.theme('default')
            .primaryPalette('red');
    })

    .config(["$translateProvider", ($translateProvider) => {
        $translateProvider.translations("es", relativeDateSpanish);
        $translateProvider.preferredLanguage('es');
    }])

    .filter("static", () => {
        
        const filter = function (input) {
            input = input.replace(/^\//,'');
            return `/static/${input}`;
        };

        return filter;

    })

    .controller("TopBarCtl", [
        "$scope",
        "$state",
        "ChangePasswordModal",
        ($scope, $state, ChangePasswordModal) => {

            $scope.searchQuery = "";

            $scope.changePassword = function () {
                var modal = ChangePasswordModal.open();
                return modal.result;
            };

            $scope.searchJob = function () {
                return $state
                    .go("jobs.search", {
                        page: 1,
                        filters: {
                            search: $scope.searchQuery
                        }
                    })
                    .then(() => {
                        $scope.searchQuery = "";
                    });
            };

        }
    ])

    .run(["$rootScope", "$state", "AccountService",
        ($rootScope, $state, AccountService) => {
        
        $rootScope.$on("$stateChangeStart", (e, to, toParam, from) => {
            console.log("start ", from, " -> ", to); 
        });

        $rootScope.$on("$stateNotFound", (e, u, from) => {
            console.log("not fund ", from, " -!-> ", u.to);
        });

        $rootScope.$on("$stateChangeSuccess", (e, t, tp, f) => {
            $rootScope.hideTeamWork = t.data && t.data.hideTeamWork;
            window.scrollTo(0, 195);
            console.log("change ", f, " -> ", t);
        });

        $rootScope.$on("$stateChangeError", (e, t, tp, f, fp, error) => {
            console.log("Error ", f, " -!->", t, ":", error);

            if (error instanceof AccountService.NotAuthUser) {
                $state.go("accounts.login");
            }

        });


    }])

    // Force textAngular to use ngSanitize
    // @see 
    // https://github.com/fraywing/textAngular/issues/842#issuecomment-132523555
    .config(["$provide", ($provide) => {
        $provide.decorator(
            'taOptions',
            [
                'taRegisterTool',
                '$delegate',
                (taRegisterTool, taOptions) => {
                    taOptions.forceTextAngularSanitize = false;
                     taOptions.toolbar = [[
                         'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'quote',
                         'bold', 'italics', 'underline', 'strikeThrough', 'ul',
                         'ol', 'redo', 'undo', 'clear', 'justifyLeft',
                         'justifyCenter', 'justifyRight', 'indent', 'outdent'],
                          ['html']];
                    return taOptions;
                }
            ]
        );
    }])

    .config(["$httpProvider", ($httpProvider) => {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])

    .config([
        "$locationProvider",
        "$stateProvider",
        "$urlRouterProvider",
        ($locationProvider, $stateProvider, $urlRouterProvider) => {
            
            $urlRouterProvider.otherwise("/home");

            $stateProvider

                .state('home', {
                    url: "/home",
                    template: homeTemplate,
                    controller: "HomeCtl",
                    data: {
                        hideTeamWork: true
                    }
                })

                .state('terms_conditions', {
                    url: "/terms_conditions",
                    templateUrl: "/templates/terms_conditions.html"
                })
                .state('about', {
                    url: "/about",
                    templateUrl: "/templates/about_us.html"
                })
            
                .state('privacy', {
                    url: "/privacy",
                    templateUrl: "/templates/privacy.html"
                })
 
                .state("contact", {
                    url: "/contact",
                    template: contactTempalte,
                    controller: "ContactCtl"
                })

                .state("test", {
                    url: "/test",
                    template: testTemplate,
                    controller: "TestCtl"
                })

            ;

            $locationProvider.html5Mode({
                enabled: true,
                requireBase: false
            });

        }
    ])

    .controller("TestCtl", [
        "$scope",
        "GeoPickerModal",
        ($scope, GeoPicker) => {

            var aItem= {pk: 1, title: "Title 1",
                        desc: "Desc1", date: "2013-03-01"};


            $scope.selectedItems = [aItem];

            $scope.table = {
                schema: {
                    $orderBy: "title",
                    $trackBy: "pk",
                    title: {
                        width: "250px",
                        sortable: true
                    },
                    desc: {
                        title: "Desciption",
                        sortable: true,
                        parser (val) {
                            return `"${val}"`;
                        }
                    },
                    date: {
                        title: "Date of...",
                        width: "150px",
                        align: "center",
                        classname: "date-field"
                    }
                },
                data: [
                    aItem,
                    {pk: 2, title: "Title 2",
                        desc: "Desc2", date: "2013-03-01"},
                    {pk: 3, title: "Title 3",
                        desc: "Desc3", date: "2013-03-01"},
                    {pk: 4, title: "Title 4",
                        desc: "Desc4", date: "2013-03-01"},
                    {pk: 5, title: "a Title 5",
                        desc: "b Desc5", date: "2013-03-01"},
                    {pk: 6, title: "z Title 6",
                        desc: "Desc6", date: "2013-03-01"},
                    {pk: 7, title: "Title 7",
                        desc: "Desc7", date: "2013-03-01"},
                    {pk: 8, title: "Title 8",
                        desc: "a Desc8", date: "2013-03-01"},
                    {pk: 9, title: "Title 9",
                        desc: "Desc9", date: "2013-03-01"},
                ]
            }; 

            $scope.completed = {
                percent: 50
            };

            $scope.filters = {
                text: {
                    value: "Search"
                },
                list: {
                    choices: [
                        {id: "a", name: "Opcion 1", cant: 13},
                        {id: "b", name: "Opcion 2", cant: 43},
                        {id: "c", name: "Opcion 3", cant: 113},
                        {id: "d", name: "Opcion 4", cant: 413},
                    ],
                    selecteds: []
                }
            };

            $scope.openGeoPicker = function (data = {}) {
                let modal = GeoPicker.open(data);

                modal.result.then((result) => {
                    console.log("GEOPICKER", result);
                });
            };            

        }
    ]);


export default app;

$(() => {

    $(document).foundation({
        tab: {
            callback : function (tab) {
                console.log(tab);
            }
        }
    });

    $('#lang a').click((e) => {
        e.preventDefault();
        e.stopPropagation();

        $('#lang-form [name="language"]')
            .val($(this).data('lang'));

        return $('#lang-form').submit();
    });
});

