"use strict";

const angular = require('angular');

const routes = require("./routes");

const postulantModule = require("../postulant");

const accountService = require("./services/account");
const authService = require("./services/auth");
const changePasswordModal = require("./modals/changepassword");
const signupController = require("./controllers/signup");
const loginController = require("./controllers/login");
const logoutController = require("./controllers/logout");
const confirmationController = require("./controllers/confirm");
const forgotController = require("./controllers/forgot");
const resetPasswordController = require("./controllers/resetpassword");

module.exports = angular.module("RoleJobs.accounts", [
    postulantModule.name,
])
    .config(routes)
    .factory("AccountService", accountService)
    .factory("AuthService", authService)
    .factory("ChangePasswordModal", changePasswordModal)
    .controller("SignupCtl", signupController)
    .controller("LoginCtl", loginController)
    .controller("LogoutCtl", logoutController)
    .controller("ConfirmCtl", confirmationController)
    .controller("ForgotPasswordCtl", forgotController)
    .controller("ResetPasswordCtl", resetPasswordController)
; 
