"use strict";

const angular = require("angular");

/**
 * Postulant CV controller
 * @memberof Postulant
 * @ngdoc controller
 * @name PostulantCvCtl
 */

const postulantCvController = function ($q, $scope, ConfirmModal,
      PostulantService, NewPEModal, NewEducationModal, NewLangModal,
                                          CroppterModal, loggedUser) {

    const OWN_VEHICLE = "own_vehicle";
    const IS_CURRENT = "is_current";
    const FIRST_NAME = "first_name";
    const LAST_NAME = "last_name";
    const LAST_UPDATE = "last_update";
    const COMPLETED_INFO = "completed_info";

    var postulantApi = new PostulantService();

    $scope.info = {
        "complete_name": `${loggedUser[FIRST_NAME]}` + 
            ` ${loggedUser[LAST_NAME]}`,
        "email": loggedUser.email,
        "last_update": loggedUser[LAST_UPDATE]
    };

    $scope.postulantData = {
        "first_name": loggedUser[FIRST_NAME],
        "last_name": loggedUser[LAST_NAME],
        "email": loggedUser.email,
        "last_update": loggedUser[LAST_UPDATE],
    };

    $scope.postulantGeoData = null; 
        
    $scope.postulantBioData = {};

    $scope.rolesData = [];

    $scope.completedProfileData = {};

    $scope.experiencesTableSchema = {
        $orderBy: "end_date",
        $trackBy: "id",
        "position_value": "Puesto", 
        "company_name": "Empresa", 
        "start_date": {
            title: "Desde",
            width: "160px",
            align: "center",
            sortable: true
        },
        "end_date": {
            title: "Hasta",
            width: "160px",
            align: "center",
            sortable: true,
            parser(val, item) {
                if (item[IS_CURRENT]) {
                    return "Actualidad";
                }

                return val;
            }
        } 
    };

    $scope.educationsTableSchema = {
        $orderBy: "end_date",
        $trackBy: "id",
       
        "level_text": {
            title: "Nivél",
            width: "200px"
        },
        institution:  "Institución",
        "start_date": {
            title: "Desde",
            width: "160px",
            align: "center",
            sortable: true
        },
        "end_date": {
            title: "Hasta",
            width: "160px",
            align: "center",
            sortable: true,
            parser(val, item) {
                if (item[IS_CURRENT]) {
                    return "Cursando";
                }

                return val;
            }
        }
    };

    $scope.languagesTableSchema = {
        $orderBy: "language_text",
        $trackBy: "language",

        "language_text": {
            title: "Idioma"
        },
        "level": {
            title: "Nivel",
            parser(val) {
                return `${val}/10`;
            }
        }
    };

    $scope.experiences = [];

    $scope.educations = [];

    $scope.languages = [];

    $scope.selecteds = {
        experiences: [],
        educations: [],
        languages: [],
    };

    $scope.apiErrors = {
        postulantForm: {},
        postulantBioForm: {},
    };

    $scope.$watchCollection("postulantData", () => {
        $scope.apiErrors.postulantForm = {};    
    });

    $scope.$watchCollection("postulantBioData", () => {
        $scope.apiErrors.postulantBioForm = {};    
    });

    $scope.$watchCollection("rolesData", (function () {
        var ts = null;

        return () => {
            if (ts) {
                clearTimeout(ts);
            }

            ts = setTimeout(() => {
                $scope.saveRoles();
            }, 600);
        };
    
    })());

    $scope.dirtForm = function (form) {
        if (form.$error && form.$error.required) {
            form.$error.required.forEach((f) => {
                f.$setDirty(); 
            });
        }

        return form;
    };
    
    $scope.displayApiErrors = function (form, data) {
        for (var i in data) {
            if (form[i]) {
                form[i].$setDirty();
                // form.$setValidity(i, false);
                $scope.apiErrors[form.$name][i] = {
                    msg: data[i][0]
                };
            }
        }
    };

    $scope.changeAvatar = function () {

        var modal = CroppterModal.open({
            width: 170,
            height: 170
        });
            
        modal.result.then((avatar) => {
            console.log("AVATAR CHANGE", avatar);
            postulantApi.changeAvatar(avatar.src)
                .then($scope.updateCompletedProfileInfo);
        });

    };

    $scope.savePostulantProfile = function (form) {

        $scope.dirtForm(form);

        if (form.$invalid) {
            return;
        }

        let data = angular.copy($scope.postulantData);

        if ($scope.postulantGeoData) {
            let geo = $scope.postulantGeoData;
            data.address = geo.address;
            data.country = geo.country;
            data.region = geo.region;
            data.city = geo.city;
        }

        postulantApi.saveProfile(data)
            .then((res) => {
                console.log(":)", res);
                $scope.updateProfile();
                $scope.updateCompletedProfileInfo();
            })
            .catch((res) => {
                if (res.data) {
                    $scope.displayApiErrors(form, res.data);
                }
            });
    };

    $scope.saveBio = function(form) {
        
        $scope.dirtForm(form);

        if (form.$invalid) {
            return;
        }

        postulantApi.saveBiograpy($scope.postulantBioData)
            .then((data) => {
                $scope.postulantBioData = data; 
                $scope.updateCompletedProfileInfo();
            })
            .catch((res) => {
                if (res.data) {
                    $scope.displayApiErrors(form, res.data);
                }
            });

    };

    $scope.saveRoles = function () {
        postulantApi.saveRoles($scope.rolesData)
            .then($scope.updateCompletedProfileInfo);
    };

    $scope.reset = function (form) {
        if (form) {
            form.$setPristine();
            form.$setUntouched();
        }
    };

    $scope.addPE = function (id = null) {
        var modal = NewPEModal.open(id);
        modal.result.then(() => {
            $scope.updateExperiences();
            $scope.updateCompletedProfileInfo();
        });
    };

    $scope.deletePE = function () {

        ConfirmModal.open("Está realmente seguro?")
            .then(() => {

                if (!$scope.selecteds.experiences.length) {
                    return;
                }

                var ids = $scope.selecteds.experiences.map(i => i.id);

                postulantApi.deleteExperiences(ids)
                    .then(() => {
                        $scope.updateExperiences();
                    })
                    .catch((res) => {
                        console.log("Error", res);
                    });

            });

    };

    $scope.addEducation = function(id = null) {
        var modal = NewEducationModal.open(id);
        modal.result.then(() => {
            $scope.updateEducations(); 
            $scope.updateCompletedProfileInfo();
        });
    };

    $scope.deleteEducations = function () {
         ConfirmModal.open("Está realmente seguro?")
            .then(() => {

                if (!$scope.selecteds.educations.length) {
                    return;
                }

                var ids = $scope.selecteds.educations.map(i => i.id);

                postulantApi.deleteEducations(ids)
                    .then(() => {
                        $scope.updateEducations();
                    })
                    .catch((res) => {
                        console.log("Error", res);
                    });

            });
     
    };

    $scope.addLanguage = function(lang = null) {
        var modal = NewLangModal.open(lang);
        modal.result.then(() => {
            $scope.updateLanguages();
            $scope.updateCompletedProfileInfo();
        });
    };

    $scope.deleteLanguages = function () {
        ConfirmModal.open("Está realmente seguro?")
            .then(() => {

                if (!$scope.selecteds.languages.length) {
                    return;
                }

                var ids = $scope.selecteds.languages.map(i => i.language);

                postulantApi.deleteLanguages(ids)
                    .then(() => {
                        $scope.updateLanguages();
                    })
                    .catch((res) => {
                        console.log("Error", res);
                    });

            });

    };

    $scope.updateInfo = function () {
        $scope.info = {
            "complete_name": `${$scope.postulantData[FIRST_NAME]}` + 
                             ` ${$scope.postulantData[LAST_NAME]}`,
            "email": $scope.postulantData.email,
            "last_update": $scope.postulantData[LAST_UPDATE]
        };
    };

    $scope.updateProfile = function () {
        
        return postulantApi.getProfile()
            .then((data) => {
                data[OWN_VEHICLE] = data[OWN_VEHICLE] ? "True" : "False";

                $scope.postulantBioData = data.biographic;
                $scope.experiences = data.experience;
                $scope.educations = data.education;
                $scope.languages = data.languages;
                $scope.rolesData = data.roles.map(x => x.pk);
                $scope.completedProfileInfo = data[COMPLETED_INFO];

                delete data.biographic;
                delete data.experience;
                delete data.education;
                delete data.languages;
                delete data.roles;
                delete data[COMPLETED_INFO];

                if (data.address && data.country && data.region) {
                    $scope.postulantGeoData = {
                        address: data.address,
                        country: data.country,
                        region: data.region,
                        city: data.city
                    };
                } else {
                    $scope.postulantGeoData = null;
                }

                delete data.address;
                delete data.country;
                delete data.region;
                delete data.address;

                $scope.postulantData = data;
                $scope.updateInfo();
            })
            .catch((err) => {
                if (err.status === 404) {
                    console.log("First time data");
                    return;
                }

                return $q.all([
                    $scope.updateBio(),
                    $scope.updateExperiences(),
                    $scope.updateEducations(),
                    $scope.updateLanguages(),
                    $scope.updateRoles(),
                    $scope.updateCompletedProfileInfo()
                ]);

            });
    };

    $scope.updateBio = function () {

        return postulantApi.getBiography()
            .then((data) => {
                $scope.postulantBioData = data;
                $scope.updateInfo();
            });

    };

    $scope.updateExperiences = function () {

        return postulantApi.getExperiences()
            .then((experiences) => {
                $scope.experiences = experiences;
                $scope.selecteds.experiences = [];
                $scope.updateInfo();
            });

    };

    $scope.updateEducations = function () {
        
        return postulantApi.getEducations()
            .then((educations) => {
                $scope.selecteds.educations = [];
                $scope.educations = educations;
                $scope.updateInfo();
            });
    };

    $scope.updateLanguages = function () {

        return postulantApi.getLanguages()
            .then((languages) => {
                $scope.selecteds.languages = [];
                $scope.languages = languages;
                $scope.updateInfo();
            });
    
    };

    $scope.updateRoles = function () {
        return postulantApi.getRoles()
            .then((roles) => {
                var pks = roles.map((role) => {
                    return role.pk;
                });

                $scope.rolesData = pks;

            });
    };

    $scope.updateCompletedProfileInfo = function () {
        return postulantApi.getCompletedProfileInfo()
            .then((info) => {
                $scope.completedProfileData = info;
            });
    };

    return $q.all([
        $scope.updateProfile()
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "ConfirmModal",
    "PostulantService",
    "PostulantNewPEModal",
    "PostulantNewEducationModal",
    "PostulantNewLanguageModal",
    "CroppterModal",
    "loggedUser",
    postulantCvController
];
