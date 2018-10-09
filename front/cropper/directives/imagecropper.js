"use strict";

/**
 * Directive to image croper editor
 * @memberof Cropper
 * @ngdoc directive
 * @name imageCropper
 */

const angular = require("angular");
const jquery = require("jquery");

const factory = function ($timeout) {
    return {
        strict: "AE",
        require: '?ngModel', 
        scope: {
            onChange: "&"
        },
        link (scope, el, attrs, ngModel) {

            const imageChange = (function () {
                var to;

                return function () {
                    if (to) {
                        $timeout.cancel(to);
                    } 

                    to = $timeout(() => {
                        if (!ngModel) {
                            return;
                        }

                        var uri = el.cropit('export', {
                            type: 'image/png',
                            quality: 1,
                            originalSize: false 
                        });

                        ngModel.$setViewValue(uri);
                        ngModel.$setDirty();
                        ngModel.$setTouched();

                        if (scope.onChange) {
                            scope.onChange({
                                $uri: uri
                            });
                        }

                    }, 500);

                };

            })();

            var options = angular.extend(angular.copy(attrs), {
                onImageLoaded: imageChange,
                onZoomChange: imageChange,
                onOffsetChange: imageChange,

            });

            el = jquery(el[0]);

            options.$preview = attrs.preview ? el.find(attrs.preview)
                                         : el.find(".cropit-preview");

            options.$fileInput = attrs.fileInput ? el.find(attrs.fileInput)
                             : el.find("input.cropit-image-input");

            options.$zoomSlider = attrs.zoomSlider ? el.find(attrs.zoomSlider)
                                : el.find("input.cropit-image-zoom-input");

            el.cropit(options);

            scope.selectImage = function () {
                options.$fileInput.click();
            };

            scope.rotateCW = function () {
                el.cropit('rotateCW');
            };

            scope.rotateCCW = function () {
                el.cropit('rotateCCW');
            };
            
            el.on('click', '[data-role="rotateleft"]', () => {
                scope.rotateCW();
            });

            el.on('click', '[data-role="rotateright"]', () => {
                scope.rotateCCW();
            });

            if (ngModel) {
                ngModel.$render = function () {
                    console.log("RENDER");
                    el.cropit('imageSrc', ngModel.$viewValue);
                };
            }

        }
    };
};

module.exports = [
    "$timeout",
    factory
];
