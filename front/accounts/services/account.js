"use strict";

module.exports = [
    "Apiv1Service",
    "AuthService",
    "extendibleBuiltin",
    "$window",
/**
 * @memberof accounts
 * @ngdoc service 
 * @name signup
 * @param {service} Apiv1service
 * @param {service} AuthService
 * @description
 *      Service to signup 
 */
function (Apiv1Service, AuthService, extendableBuiltin) {

    class NotAuthUser extends extendableBuiltin(Error) {
        constructor(msg) {
            super(msg);
            this.name = "NotAuthUser";
        }
    }

    const signup = function (data) {
        data = Apiv1Service.normalize(data);
        data.role = data.role.value;

        var api = Apiv1Service.getInstance();
        return api.post('accounts/signup', data);
    };

    const login = function (data) {
        data = Apiv1Service.normalize(data);
        return Apiv1Service.getInstance().post('accounts/authlogin/', data)
            .then((data) => {
                AuthService.auth(data.key);
            });
    };

    const facebook = function () {
        return Apiv1Service.getInstance().get("accounts/facebook/login/")
            .then((response) => {
                return response.data;
            });
    };

    const google = function () {
        return Apiv1Service.getInstance().get('accounts/google/login/')
            .then((response) => {
                return response.data;
            });
    };

    const linkedin = function () {
        return Apiv1Service.getInstance().get('accounts/linkedin/login/')
            .then((response) => {
                return response.data;
            });
    };

    const logout = function () {
        return Apiv1Service.getInstance().post("accounts/authlogout/")
            .then((response) => {
                return response.data.success ;
            });
    };

    const confirmAccount = function (data) {
        return Apiv1Service.getInstance().post("accounts/confirm", data)
            .then((response) => {
                return !!response.data.success;
            });
    };

    const getLoggedUser = function () {
        return Apiv1Service.getInstance().get("accounts/")
            .then((response) => {
                return response.data;
            })
            .catch((response) => {
                if (response.status === 403) {
                    throw(new NotAuthUser(response.data));
                }

                throw response;
            });
    };

    const resetPassword = function (email) {
        return Apiv1Service.getInstance()
            .post("accounts/authpassword/reset/", { email })
            .then((response) => {
                return response.data;
            });
    };

    const verifyResetPasswordEmail = function (email) {
        return Apiv1Service.getInstance()
            .post("accounts/verifyresetpasswordemail/", { email })
            .then((response) => {
                return response.data;
            });
    };

    const confirmResetPassword = function (uid, token, password) {

        return Apiv1Service.getInstance()
            .post("accounts/authpassword/reset/confirm/", {
                uid,
                token,
                "new_password1": password,
                "new_password2": password
            })
            .then((response) => {
                return response.data;
            });
    };

    const changePassword = function (data) {
        return Apiv1Service.getInstance()
            .post("accounts/authpassword/change/", data)
                .then((response) => {
                    return response.data;
                });
    };

    return {
        signup,
        login,
        facebook,
        google,
        linkedin,
        logout,
        confirmAccount,
        getLoggedUser,
        NotAuthUser,
        resetPassword,
        verifyResetPasswordEmail,
        confirmResetPassword,
        changePassword
    };

}];
