var chatApp = angular.module('chatApp', ['ngCookies', 'Alertify']);
chatApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

chatApp.run(function ($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
});

chatApp.controller('app_controller', function ($scope) {
    //
});

chatApp.controller('chat_controller', function ($scope, $http, Alertify) {
    $scope.formData = {};
    $scope.messages = [];
    $scope.submitForm = function () {
        var sendData = new FormData(document.getElementById("messageForm"));
        for (var key in $scope.formData) {
            if (!sendData.has(key) && $scope.formData[key] != false) {
                sendData.append(key, $scope.formData[key]);
            }
        }
        $http({
            url: '/save_messages/',
            method: "POST",
            data: sendData,
            headers: {'Content-Type': undefined},
            processData: false
        }).then(function successCallback(response) {
            $scope.get_message(response.data.id);
            json_data = angular.fromJson(response.data);
            if (typeof(json_data['error']) != 'undefined') {
                alert('No se pudo guardar el mensaje');
            } else {
                $scope.formData = {};
            }
        }, function errorCallback(response) {
        });
    };


    $scope.load_data = function(url, scope_var, concat=false) {
        if(!url) return;
        $scope['loading_' + scope_var] = true;
        $http({
            url: url,
            method: "GET",
            data: {},
            headers: {'Content-Type': 'application/json'},
        }).then(function (response) {
            if(concat){
                $scope[scope_var] = $scope[scope_var].concat(response.data.results);
            } else {
                $scope[scope_var] = response.data.results;
            }
            $scope['next_' + scope_var] = response.data.next;
            $scope['previous_' + scope_var] = response.data.previous;
            $scope['loading_' + scope_var] = false;
        }, function errorCallback(response) {
            $scope['loading_' + scope_var] = false;
        });
    }

    $scope.get_message = function(id){
        $http({
            url: '/api/1/messages/get_object/?pk='+id,
            method: "GET",
            data: {},
            headers: {'Content-Type': 'application/json'},
        }).then(function (response) {
            $scope.messages.unshift(response.data);
        }, function errorCallback(response) {
        });
    }

    $scope.get_last_message = function(){
        if($scope.messages.length){
            return $scope.messages[0];
        }
    }

    $scope.update_messages = function(){
        last_message = $scope.get_last_message();
        $http({
            url: '/api/1/messages/new_messages/?last_message_id='+ last_message.id,
            method: "GET",
            data: {},
            headers: {'Content-Type': 'application/json'},
        }).then(function (response) {
            if(response.data){
                $scope.load_data('/api/1/messages/', 'messages');
            }
        }, function errorCallback(response) {
        });
    }

    $scope.delete_message = function(id){
        Alertify.confirm('¿Realmente desea eliminar este mensaje?')
        .then(function () {
            $scope.delete_message_api(id);
        }, function () {
        });
    }

    $scope.delete_message_api = function(id){
        $http({
            url: '/api/1/messages/delete/?pk=' + id,
            method: "GET",
            data: {id},
            headers: {'Content-Type': 'application/json'},
        }).then(function (response) {
            if(response.status===204){
                $scope.load_data('/api/1/messages/', 'messages');
                Alertify.alert('Mensaje eliminado');
            }
        });
    }
    
    angular.element(document).ready(function () {
        setInterval($scope.update_messages, 10000);
        setInterval($scope.load_data, 30000, '/api/1/auth_user/', 'users_list');
        jQuery(function($) {
            $('.msg_history').on('scroll', function() {
                if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
                    $scope.load_data($scope.next_messages, 'messages', true, false);
                }
            })
        });
    });
});
