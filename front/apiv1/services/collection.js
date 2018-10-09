"use strict";

/**
 * Api collection connector 
 * @memberof ApiV1
 * @ngdoc service
 * @name CollectionService 
 */

const angular = require("angular");

const factory = function (Apiv1Service, RecordSet) {

    class CollectionRecordSet extends RecordSet.BaseRecordSet {

        constructor(collection, data, options = {}, page = 1) {
            super(data, options);
            this._collection = collection;
            this._page = page;
        }

        _processItem(op, item) {
            var pk = this._options.pk || 'pk';

            switch (op) {
                case "delete":
                    return this._collection.delete(item[pk]);
                case "detailed":
                    return this._collection.get(item[pk])
                        .then((response) => {
                            return response.data;
                        });
                case "save":
                    return this._collection.put(item[pk], item);
                default:
                    throw new Error("Unknow operation");
            }
        
        }

        _extendItem(item) {
            item.$delete = () => {
                return this._processItem('delete', item);
            };

            item.$detailed = () => {
                return this._processItem('detailed', item);
            };

            item.$save = () => {
                return this._processItem('save', item);
            };

            return item; 
        }

        _processItems(items) {

            return items.map((item) => {
                return this._extendItem(item);
            });
        }

        create(data) {
            return this._collection.post(data);
        }

        getNextPage(options = {}) {
            return this._collection.fetch(this._page +1, options);
        }

        get collection() {
            return this._collection;
        }

    }

    class Collection {
        
        constructor(path, options = {}) {
            this._path = path;
            this._options = options;
            this._options.pk = options.pk || 'pk';
            this._options.http = options.http || {};
            this._api = Apiv1Service.getInstance();
        }

        _getRecordSetClass() {
            return CollectionRecordSet;
        }

        _get(path, params = {}) {
            return this._api.get(path, params);
        }

        get(subpath, params = {}) {
            var path = `${this._path}/${subpath}`;
            return this._get(path, params);
        }

        post(data, params = {}, subpath = null) {
            var path = this._path;
            
            if (subpath) {
                path += `/${subpath}`;
            }

            return this._api.post(path, data, params);
        }
        
        put(data, params = {}, subpath = null) {
            var path = this._path;
            
            if (subpath) {
                path += `/${subpath}`;
            }

            return this._api.put(path, data, params);
        }

        getItem(id, params = {}) {

            return this.get(id, params, this._options.http)
                .then((response) => {

                    if (!response.data) {
                        throw new Error("Invalid response");
                    }

                    var RS = this._getRecordSetClass();
                    var rs = new RS(this, {
                        results: [response.data]
                    });

                    return rs.items[0];

                });
        }

        fetch(page = 1, options = {}) {
            var path = `${this._path}`;
            
            var httpOptions = angular.extend(
                {},
                this._options.http,
                options);
            
            var params = angular.extend({
                page: page}, options.params || {});

            var RecordSetClass = this._getRecordSetClass();

            return this._get(path, params || {}, httpOptions)
                .then((response) => {
                    if (!response.data) {
                        throw new Error("Invalid response");
                    }

                    return new RecordSetClass(
                        this, response.data, this._options, page);

                });
        }

        get path () {
            return this._path;
        }

    }

    return {
        CollectionRecordSet,
        Collection
    };

};

module.exports = [
    "Apiv1Service",
    "RecordSet",
    factory
];
