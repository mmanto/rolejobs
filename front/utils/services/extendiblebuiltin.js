"use strict";

/**
 * Extendible Builting
 * @see http://log.exodica.com.ar/3p
 * @ngdoc service 
 * @name ExtendibleBuiltin
 * @memberof Utils
 */

const factory = function () {

    var extendableBuiltin = function (cls) {

        var ExtClass = function () {
            cls.apply(this, arguments);
        };

        ExtClass.prototype = Object.create(cls.prototype);

        Object.setPrototypeOf(ExtClass, cls);

        return ExtClass;

    };

    return extendableBuiltin;

};

module.exports = factory;
