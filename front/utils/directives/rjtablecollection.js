"use strict";

/**
 * RJ's style table Collection 
 * @memberof Utils
 * @ngdoc directive
 * @name rjTableModel
 */

const angular = require("angular");

const rjTableCollectionFactory = function() {

    const getId = (function () {
        var last = 0;

        return function () {
            return last++;
        };
    
    })();

    const template = `
        <div rj-table>
            <div class="row header">
                <div 
                    ng-if="selectable"
                    rj-table-field 
                    class="select-all-box"
                    align="center"
                >
                    <input
                        type="checkbox"
                        ng-model="selectall"
                        ng-click="selectAll()"
                    >
                </div>
                <div 
                    ng-if="actions.length"
                    rj-table-field 
                    class="actions-button-header"
                ></div>
                <div
                    rj-table-field 
                    ng-repeat="item in headers track by item.name"
                    ng-style="item.widthStyle"
                    ng-class="{sortable: item.sortable}"
                    align="{{item.align}}"
                >
                    <div class="content" ng-click="sort(item)">
                        {{ item.title }}
                    </div>
                </div>
               
            </div>
            <div
                class="row item-row"
                ng-repeat="item in items |
                           orderBy:orderField:orderReverse track by item.id"
                ng-class="{selected: item.selected}"
            >
                <div 
                    ng-if="selectable"
                    rj-table-field 
                    class="select-box"
                    align="center"
                >
                    <input
                        type="checkbox"
                        ng-model="item.selected"
                        ng-click="select()"
                    >
                </div>
                <div 
                    ng-if="actions.length"
                    rj-table-field 
                    class="actions-button-box"
                >
                    <a
                        dropdown-toggle="#actions-of-{{uuid}}-{{item.id}}"
                    >
                        <i
                            class="fa fa-play-circle fa-rotate-90"
                            aria-hidden="true"
                        ></i>
                    </a> 
                    <ul
                        id="actions-of-{{uuid}}-{{item.id}}"
                        class="f-dropdown"
                    >

                        <li ng-repeat="action in actions">
                         <a 
                            ng-click="clickAction(action, item)"
                         >{{action.name}}</a>
                        </li>
                    </ul>
                </div>
                <div
                    rj-table-field 
                    ng-repeat="field in item.fields track by field.$header.name"
                    ng-style="field.$header.widthStyle"
                    align="{{field.$header.align}}"
                    ng-class="field.$header.extraClass"
                    ng-click="clicked(item)"
                >
                    <div class="content">{{ field.content }}</div>
                </div>
            </div>
        </div>
    `;

    return {
        strict: "EA",
        replace: true,
        template: template,
        require: '?ngModel', 
        scope: {
            collectionData: "=",
            collectionSchema: "=",
            collection: "=",
            onClick: "&"
        },
        link (scope, el, attrs, ngModel) {
            var unregisterInit;

            scope.uuid = (new Date()).getTime().toString(36);
            scope.data = [];
            scope.schema = {};
            scope.headers = [];
            scope.items = [];
            scope.trackBy = attrs.trackBy || "id";
            scope.selectable = typeof attrs.selectable !== "undefined";
            scope.selectall = false;
            scope.commands = {};
            scope.orderField = attrs.orderBy ? `__${attrs.orderBy}` : "";
            scope.actions = [];

            scope.getStyle = function (size) {

                if (typeof size === "number" ||
                    (typeof size === "string" &&
                    size.match(/^[0-9]$/i))) {

                    return {
                        "-moz-flex": `${size}`,
                        "-webkit-flex":`${size}`,
                        "flex":`${size}`
                    };

                } else {
                    return {
                        "width": `${size}`
                    };
                } 

            };

            scope.sort = function (item) {
                if (item.sortable) {
                    if (scope.orderField === `__${item.name}`) {
                        scope.orderReverse = !scope.orderReverse;
                    } else {
                        scope.orderField = `__${item.name}`;
                        scope.orderReverse = false;
                    }
                }
            };

            scope.setValue = function (internal) {
                if (ngModel) {
                    ngModel.$setViewValue(scope.selectedItems);

                    if (internal) {
                        ngModel.$setDirty();
                        ngModel.$setTouched();
                    }
                }
            };

            scope.select = function (internal = false) {
                scope.selectedItems = [];

                scope.selectedItems = scope.items
                    .filter((item) => {
                        return item.selected;
                    })
                    .map((item) => {
                        return item.odata;
                    });
                
                scope.setValue(internal);

            };

            scope.selectAll = function () {
                scope.selectall = !scope.selectall;

                scope.items.forEach((item) => {
                    item.selected = scope.selectall;
                });

                scope.select();

            };

            scope.clickAction = function(action, item) {
                action.action(item.odata);
            };

            scope.clicked = function (item) {
                if (scope.onClick) {
                    scope.onClick({
                        "$item": item.odata,
                        "$selected": item.selected
                    });
                }
            };

            scope.updateSchema = function (schema) {

                if (!schema) {
                    return;
                }

                scope.schema = schema;
                scope.headers = [];

                if (schema.$trackBy) {
                    scope.trackBy = schema.$trackBy;
                }

                if (schema.$orderBy) {
                    scope.orderField = `__${schema.$orderBy}`;
                }

                if (schema.$orderReverse) {
                    scope.orderReverse = schema.$orderReverse;
                }

                if (schema.$actions) {

                    angular.forEach(schema.$actions, (v, k) => {
                        scope.actions.push({
                            name: k,
                            action: v
                        });
                    });
                }

                scope.orderReverse = !!scope.orderReverse;

                angular.forEach(schema, (sitem, i) => {

                    if (!i.match(/^[\w]/i)) {
                        return;
                    }

                    if (typeof sitem !== "object") {
                        if (typeof sitem === "boolean") {
                            sitem = {
                                title: i
                            };
                        } else {
                            sitem = {
                                title: `${sitem}` 
                            };
                        }
                    }

                    scope.headers.push({
                        name: i,
                        title: sitem.title || i,
                        size: sitem.width || 1,
                        field: sitem.field || i,
                        widthStyle: scope.getStyle(sitem.width || 1),
                        align: sitem.align || 'left',
                        extraClass: sitem.classname || '',
                        sortable: sitem.sortable || false,
                        parser(value, vitem) {
                            if (sitem.parser) {
                                return sitem.parser(value, vitem);
                            } else {
                                return value; 
                            }
                        },
                        action() {
                            if (sitem.action) {
                                sitem.action(sitem);
                            }
                        }
                    });

                });
                
                console.log(scope.headers);

            };

            scope.updateData = function (data) {

                if (typeof data === "undefined") {
                    return;
                }

                scope.data = data;
                scope.items = data.map((item) => {
                    var orders = [];
                    var selected = false;

                    if (scope.selectable) {
                        if (scope.selectedItems.indexOf(item) !== -1) {
                            selected = true;
                        }
                    }

                    var res = {
                        id: scope.trackBy ? item[scope.trackBy] : getId(),
                        selected: selected,
                        odata: item,
                        fields: scope.headers.map((h) => {

                            var content = h.parser(item[h.field], item);

                            if (h.sortable) {
                                orders.push({
                                    name: h.name,
                                    content: content
                                });
                            }

                            return {
                                $header: h,
                                content: content 
                            };
                        })
                    };

                    orders.forEach((o) => {
                        res[`__${o.name}`] = o.content;
                    });

                    return res;

                });

                scope.select(true);
                console.log("items", scope.items);

            };

            const init = function (options) {
                unregisterInit();

                console.log("Init with", options);

                if (ngModel) {
                    scope.selectedItems = options.value;
                    ngModel.$setViewValue(options.value);
                }

                scope.updateSchema(options.schema);
                scope.updateData(options.data);

                scope.$watchCollection("collection.data", (newValue) => {
                    scope.updateData(newValue);
                }); 

                scope.$watchCollection("collectionData", (newValue) => {
                    scope.updateData(newValue);
                });

                scope.$on("rjtablecollection:forceupdate", () => {
                    scope.updateData(scope.data);
                });

            };

            unregisterInit = scope.$watch(() => {
                var schema, data, value;

                if (scope.colleciton && scope.collectionSchema) {
                    throw new Error("Only define collection or " +
                                    "collectionSchema, not both");
                }

                if (scope.collection) {
                    schema = scope.collection.schema;
                    data = scope.colleciton.data;
                } else if (scope.collectionSchema) {
                    schema = scope.collectionSchema;
                }

                if (scope.collectionData) {
                    data = scope.collectionData;
                }

                if (ngModel) {
                    value = ngModel.$modelValue;
                }

                if (!value) {
                    value = [];
                }

                return {
                    schema,
                    data,
                    value
                };

            }, init);


        }
    };
};

module.exports = rjTableCollectionFactory;
