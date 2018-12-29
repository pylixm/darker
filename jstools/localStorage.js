/****localStorage functional****
 ****    author: jinlong    ****
 */
var store  = (function (window){
    if(!window.localStorage){
        alert("无法开启浏览器的localStorage功能, 请您更换浏览器");
        return;
    }

    var _set = function(key, value){
        value = JSON.stringify(value);
        window.localStorage.setItem(key, value);
    };

    var _get = function(key){
        var value = window.localStorage.getItem(key);
        return JSON.parse(value);
    };

    var _pop = function(key){
        var value = window.localStorage.getItem(key);
        _remove(key);
        return JSON.parse(value);
    };

    var _remove = function(key){
        window.localStorage.removeItem(key)
    };

    var _clear = function(){
        window.localStorage.clear();
    };

    var _length = function(){
        return window.localStorage.length;
    };



    return{
        setKey: _set,
        getKey: _get,
        removeKey: _remove,
        clear: _clear,
        length: _length,
        pop: _pop
    }

})(window);