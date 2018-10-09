"use strict";

/**
 * Recordset to help the pagination results
 * @memberof ApiV1
 * @ngdoc service
 * @name RecordSet
 */

const factory = function () {

    class BaseRecordSet {
       
        constructor(data, options = {}) {
            this._items = this._processItems(data.results) || [];
            this._totalLength = data.count || 0;
            this._options = options;
        }

        _processItems(items) {
            return items;
        }

        toArray() {
            return this._items;
        }

        map(fn) {
            return this._items.map(fn);
        }

        find(fn) {
            return this._items.find(fn);
        }

        filter(fn) {
            return this._items.find(fn);
        }

        get items() {
            return this._items;
        }

        get length() {
            return this._items.length;
        }
        
        get totalLength() {
            return this._totalLength;
        }

    }

    return {
        BaseRecordSet,
    };

};

module.exports = [
    factory
];
