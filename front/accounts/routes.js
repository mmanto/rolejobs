"use strict";

const signupTemplate = require("account/signup.html");
const confirmationSentTemplate = require("account/verification_sent.html");
const confirmationTemplate = require("account/confirmation.html");
const confirmedTemplate = require("account/confirmed.html");
const confirmationfailTemplate = require("account/confirmationfail.html");
const loginTemplate = require("account/login.html");
const logoutTemplate = require("account/logout.html");
const forgotPasswordTemplate = require("account/forgot_password.html");
const resetPasswordTemplate = require("account/reset_password.html");

module.exports = ["$stateProvider", ($stateProvider) => {

    $stateProvider
        .state("accounts", {
            url: "/accounts",
            abstract: true,
            template: '<div ui-view="accounts-main"></div>'
        })

        .state('accounts.signup', {
            url:"/signup",
            views: {
                "accounts-main": {
                    template: signupTemplate,
                    controller: "SignupCtl"
                }
            }
        })
    
        .state('accounts.confirmationsent', {
            url: "/confirmationsent",
            data: {
                email: "??"
            },
            views: {
                "accounts-main": {
                    template: confirmationSentTemplate
                }
            }
        })

        .state('accounts.confirm', {
            url: '/confirm/:id/:hash',
            views: {
                "accounts-main": {
                    template: confirmationTemplate,
                    controller: "ConfirmCtl"
                }
            }
        })

        .state('accounts.confirmed', {
            url:"/confirmed",
            views: {
                "accounts-main": {
                    template: confirmedTemplate,
                }
            }
        })

        .state('accounts.confirmationfail', {
            url:"/confirmationfail",
            views: {
                "accounts-main": {
                    template: confirmationfailTemplate,
                }
            }
        })

        .state("accounts.login", {
            url:"/login",
            views: {
                "accounts-main": {
                    template: loginTemplate,
                    controller: "LoginCtl"
                }
            }
        })

       
        .state("accounts.facebook", {
            url:"/facebook/login/",
            views: {
                "accounts-main": {
                    controller: "SignupCtl"
                }
            }
        })
       
        .state("accounts.google", {
            url:"/google/login/",
            views: {
                "accounts-main": {
                    controller: "SignupCtl"
                }
            }
        })
        
        .state("accounts.linkedin", {
            url:"/linkedin/login/",
            views: {
                "accounts-main": {
                    controller: "SignupCtl"
                }
            }
        })
        
        .state("accounts.logout", {
            url:"/logout",
            views: {
                "accounts-main": {
                    template: logoutTemplate,
                    controller: "LogoutCtl"
                }
            }
        })

        .state("accounts.forgot", {
            url: "/forgot",
            views: {
                "accounts-main": {
                    template: forgotPasswordTemplate,
                    controller: "ForgotPasswordCtl"
                }
            }
        })

        .state("accounts.resetPassword", {
            url: "/reset_password/:uid/:token",
            views: {
                "accounts-main": {
                    template: resetPasswordTemplate,
                    controller: "ResetPasswordCtl"
                }
            }
        })

    ;
}];
