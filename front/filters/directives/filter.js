"use strict";

/**
 * Filter directive, for filters objects
 * @memberof Filters
 * @ngdoc directive
 * @name rjFilter
 */

const template = require("filters/filter.html");

const castBoolean = function (val) {

    if (typeof val === "string") {
        if (val.trim() === "") {
            return false;
        }

        return !val.match(/(false|0+|no)/i);
    }

    return val;

};

const factory = function () {

    const VALID_TYPES = [
        'searchbox',
        'list'
    ];

    const getFakeId = (function () {
        var lastId = 0;

        return function () {
            return lastId--;
        };

    })();

    return {
        strict: "E",
        replace: true,
        require: '?ngModel',
        template,
        scope: {
            type: "@",
            title: "=",
            choices: "=?",
            onFilterChange: "&?"
        },
        link (scope, el, attrs, ngModel) {
            var unregisterInit;

            if (VALID_TYPES.indexOf(attrs.type) === -1) {
                throw new Error(`Invalid rjFilter type ${attrs.type}`);
            }

            scope.placeholder = attrs.placeholder || "";
            scope.titleClass = attrs.titleClass || "";
            scope.itemPk = attrs.itemPk || null;
            scope.items = [];
            scope.multiSelect = !!castBoolean(attrs.multiSelect);
            scope.searchQuery = {
                value: ""
            };
            scope.selectedItems = [];
            scope.selectedItem = null;
            scope._prevValue = null;

            scope.value = null;

            scope.getItemPk = function (item) {
                var $id;

                if (scope.itemPk &&
                    typeof item[scope.itemPk] !== "undefined") {
                    $id = item[scope.itemPk];
                } else {
                    $id = getFakeId();
                }

                return $id;
            };

            scope.updateItems = function (items) {

                if (!items) {
                    return;
                }

                scope.items = items.map((item) => {
                    return {
                        $id: scope.getItemPk(item),
                        content: item
                    };

                });
            };

            scope.clicked = function (item) {
                var exists;

                if (scope.multiSelect) {
                    exists = scope.selectedItems
                        .find(x => x.$id === item.$id);

                    if (exists) {
                        return;
                    }

                    scope.selectedItems.push(item);
                    scope.setValue(
                        scope.selectedItems.map(x => x.content),
                        true);

                } else {
                    scope.selectedItem = item.content;
                    scope.setValue(scope.selectedItem, true);
                }
            };

            scope.setViewValue = function (value) {
                if (scope.multiSelect) {
                    var values = value.map((v) => {
                        return {
                            $id: scope.getItemPk(v),
                            content: v
                        };
                    });

                    scope._prevValue = scope.selectedItems;
                    scope.selectedItems = values;
                } else {
                    scope._prevValue = scope.selectedItem;
                    if (value) {
                        scope.selectedItem = {
                            $id: scope.getItemPk(value),
                            content: value
                        };
                    } else {
                        scope.selectedItem = null;
                    }
                }

            };

            scope.setValue = function (value, internal = false,
                                                forceApply = false) {
                if (scope._prevValue === value) {
                    return;
                }

                switch (scope.type) {
                    case "searchbox":
                        if (!internal && !forceApply) {
                            scope.searchQuery.value = value;
                        }
                        break;
                    case "list":
                        break;
                }

                scope._prevValue = value;

                if (ngModel) {
                    ngModel.$setViewValue(value);

                    if (internal) {
                        ngModel.$setDirty();
                        ngModel.$setTouched();
                    }
                }

                if (scope.onFilterChange) {
                    scope.onFilterChange({
                        $value: value
                    });
                }

            };
            
            const init = function (options) {
                unregisterInit();

                if (ngModel) {
                    ngModel.$setViewValue(options.value);
                    ngModel.$viewChangeListeners = [() => {
                        scope.setViewValue(ngModel.$viewValue);
                    }];

                    ngModel.$render = function () {
                        scope.setViewValue(this.$viewValue);
                    };

                    scope.setValue(ngModel.$viewValue);
                }

                if (scope.type === "list") {
                    scope.$watchCollection("choices", (newValue) => {
                        scope.updateItems(newValue, false, true);
                    });
                }

                if (scope.type === "searchbox") {
                    scope.$watch("searchQuery.value", (newValue) => {
                        return scope.setValue(newValue, true);
                    });
                }

            };

            unregisterInit = scope.$watch(() => {
                var value;

                if (ngModel) {
                    value = ngModel.$modelValue;
                }

                if (!value) {
                    value = null;
                }

                return {
                    value
                };

            }, init);

        }
    };

};

module.exports = factory;
