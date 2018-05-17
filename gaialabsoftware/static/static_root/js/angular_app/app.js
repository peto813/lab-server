


var gaiaApp = angular.module("gaiaApp",
 [ 'ui.router', 
'ui.bootstrap', 
'ngMessages', 
'appControllers',
'cfp.hotkeys',
'appServices', 
'appDirectives', 
'gaiaAppFilters',
//'ezfb', 
//'ngSanitize', 
//'chart.js',
'ngFileUpload'
]);//, 'hmShipControllers', 'hmShipServices'
  
 
gaiaApp.config(function($stateProvider, $urlRouterProvider, $locationProvider){
    $stateProvider
        .state('index', {
            url:'/',
            templateUrl : 'static/templates/views/index.html',
            isLogin: false,
            data : { pageTitle:' GaiaSoft | Ingreso' },
            controller : 'indexController',
            resolve: {
                context: function($http) {
                    var url = 'api/initial/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }

            }
        })
        .state('resultados', {
            url:'/resultados',
            templateUrl : 'static/templates/views/resultados.html',
            isLogin: true,
            data : { pageTitle: 'GaiaSoft | Resultados' },
            controller : 'resultadosController',
            resolve: {
                resultados: function($http) {
                    var url = 'api/resultados/?impreso=True';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }

            }
        })
        .state('codigos', {
            url:'/codigos',
            templateUrl : 'static/templates/views/codigos.html',
            isLogin: true,
            data : { pageTitle: 'GaiaSoft | Codigos' },
            controller : 'codigosController',
            resolve: {
                codigos: function($http) {
                    var url = 'api/codigos/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }

            }
        })
        .state('inicio', {
            url:'/inicio',
            templateUrl : 'static/templates/views/inicio.html',
            isLogin: true,
            data : { pageTitle: 'GaiaSoft | Inicio' },
            controller : 'homeController',
            resolve: {
                estudios: function($http, $location) {
                    console.log($location.search())
                    var url = 'api/estudios/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                },
                agregar_estudio:function($location){
                    return $location.search();
                }

            }
        })


        .state('reportes', {
            url:'/reportes',
            templateUrl : 'static/templates/views/reportes.html',
            isLogin: true,
            data : { pageTitle: 'GaiaSoft | Reportes' },
            controller : 'reportesController',
            resolve: {
                context: function($http) {
                    var url = 'api/reportes/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })

        .state('paciente_post_pago', {
            url:'/paciente_post_pago',
            templateUrl : 'static/templates/views/pacientePostPago.html',
            isLogin: true,
            controller : 'pacientePostPagoController',
            resolve: {
                estudios: function($http) {
                    var url = 'api/paciente_post_pago/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        
                        return response.data;
                    })
                }

            }
        })

        .state('pacientes', {
            url:'/pacientes',
            templateUrl : 'static/templates/views/pacientes.html',
            isLogin: true,
            controller : 'pacientesController',
            data : { pageTitle: 'GaiaSoft | Pacientes' },
            resolve: {
                listaPacientes: function($http) {
                    var now_date = new Date()
                    var timestamp_lte = new Date();
                    var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    var url = 'api/pacientes/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
                    //var url = 'api/pacientes/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                },
                firstPatientDate: function($http) {
                    //var now_date = new Date()
                    //var timestamp_lte = new Date();
                    //var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    //var url = 'api/pacientes?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
                    var url = 'api/first_patient/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                },


            }
        })
        .state('estudios', {
            url:'/estudios',
            templateUrl : 'static/templates/views/estudios.html',
            isLogin: true,
            controller : 'estudiosController',
            data : { pageTitle: 'GaiaSoft | Estudios' },
            resolve: {
                listaEstudios: function($http) {
                    var now_date = new Date()
                    var timestamp_lte = new Date();
                    var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    var url = 'api/estudios_model/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()+'&impreso=True'
                    //var url = 'api/pacientes/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        console.log(response)
                        return response.data;
                    })
                }
            }
        })
        .state('facturas', {
            url:'/facturas',
            templateUrl : 'static/templates/views/facturas.html',
            isLogin: true,
            controller : 'facturasController',
            data : { pageTitle: 'GaiaSoft | Estudios' },
            resolve: {
                listaFacturas: function($http) {
                    var now_date = new Date()
                    var timestamp_lte = new Date();
                    var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    var url = 'api/facturas/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()+'&impreso=True'
                    //var url = 'api/pacientes/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })

        .state('postpago', {
            url:'/postpago',
            templateUrl : 'static/templates/views/postpago.html',
            isLogin: true,
            controller : 'postPagoController',
            data : { pageTitle: 'GaiaSoft | Clientes Post-Pago' },
            resolve: {
                clientesPostPago: function($http) {
                    var url = 'api/clientes_postpago/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })



        .state('estadisticas', {
            url:'/estadisticas',
            templateUrl : 'static/templates/views/estadisticas.html',
            isLogin: true,
            controller : 'estadisticasController',
            data : { pageTitle: 'GaiaSoft | Estadisticas' }
            // resolve: {
            //     bankAccounts: function($http) {
            //         var url = 'api/bankaccounts/';
            //         return $http({ 
            //             method: 'GET', 
            //             url: url
            //         }).then(function(accounts){
            //             return accounts.data;
            //         })
            //         // $http.get('api/bankaccounts/').success(function(accounts){
            //         //     return 'peo'
            //         // })
            //     }
            // }
        })
        .state('precios', {
            url:'/precios',
            templateUrl : 'static/templates/views/precios.html',
            data : { pageTitle: 'GaiaSoft | Precios' },
            controller : 'preciosController',
            isLogin: true,
            resolve: {
                precios: function($http) {
                    var url = 'api/precios/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(accounts){
                        return accounts.data;
                    })
                }
            }

        })  

//         .state('paymentmethod', {
//             url:'/paymentmethod',
//             templateUrl : 'static/templates/userapp/payments/paymentmethod.html',
//             data : { pageTitle: 'Choose Payment Method' },
//             controller : 'paymentMethodController',
//             isLogin: true,
//             resolve: {
//                 shoppingCart: function($window, $location) {
//                     var shoppingCart = JSON.parse( $window.sessionStorage.getItem('shoppingCart') );
//                     if( shoppingCart.length < 1 ){
//                         $location.path( 'home' )
//                     }else{
//                        return shoppingCart; 
//                     }
                    
//                 }
//             }

//         })  


//         .state('paymenthistory', {
//             url:'/paymenthistory',
//             templateUrl : 'static/templates/userapp/paymenthistory/paymenthistory.html',
//             isLogin: true,
//             data : { pageTitle: 'Payment History' },
//             controller : 'paymentHistoryController',
//             resolve: {
//                 // OrderBook: function($http) {
//                 //     var url = 'api/orderbook/';
//                 //     return $http({ 
//                 //         method: 'GET', 
//                 //         url: url
//                 //     }).then(function(response){
//                 //         return response.data;
//                 //     })
//                 // },
//                 paymentHistory: function($http) {
//                     var now_date = new Date()
//                     var timestamp_lte = new Date();
//                     var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
//                     var url = 'api/payments?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString();
//                     //var url = 'api/payments?time';
//                     return $http({ 
//                         method: 'GET', 
//                         url: url
//                     }).then(function(response){
//                         return response.data;
//                     })
//                 }
//             }


//         })

//         .state('orderhistory', {
//             url:'/orderhistory',
//             templateUrl : 'static/templates/userapp/orderhistory/orderhistory.html',
//             isLogin: true,
//             data : { pageTitle: 'Auction Products' },
//             controller : 'orderHistoryController'
//         })

//         .state('orderbook', {
//             url:'/orderbook',
//             templateUrl : 'static/templates/userapp/orderbook/orderbook.html',
//             controller : 'orderBookController',
//             data : { pageTitle: 'OrderBook' },
//             isLogin: true,
//             // resolve: {
//             //     shoppingCart: function($window) {
//             //         return JSON.parse($window.sessionStorage.getItem('shoppingCart'));
//             //     }
//             // }
//             resolve: {
//                 OrderBook: function($http) {

//                     var now_date = new Date()
//                     var timestamp_lte = new Date();
//                     var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
//                     var url = 'api/services?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
//                     return $http({ 
//                         method: 'GET', 
//                         url: url
//                     }).then(function(response){
//                         return response.data;
//                     })
//                 },
//                 shoppingCart: function($window) {
//                     return JSON.parse($window.sessionStorage.getItem('shoppingCart'));
//                 }
//             }

//         })

//         .state('index', {
//             url:'/',
//             templateUrl : 'static/templates/userapp/index/index.html',
//             controller : 'indexController',
//             data : { pageTitle: 'Welcome' },
//             isLogin: false
//         })
//         .state('profile', {
//             url:'/profile',
//             templateUrl : 'static/templates/userapp/profile/profile.html',
//             controller : 'profileController',
//             isLogin: true,
//             data : { pageTitle: 'User Profile' },
//             resolve: {
//                 sessionData: function($window) {
//                     return JSON.parse($window.sessionStorage.getItem('userDataString'));
//                     // var url = 'api/auctionproducts/';
//                     // var params = { 'q' :  'maintenance'};
//                     // return $http({ 
//                     //     method: 'GET', 
//                     //     url: url,
//                     //     params:params,
//                     // }).then(function(response){
//                     //     return response.data;
//                     // })
//                 }
//             }
//             //JSON.parse($window.sessionStorage.getItem('userDataString'))
//         })
//         .state('maintenance', {
//             url:'/maintenance',
//             templateUrl : 'static/templates/userapp/maintenance/maintenance.html',
//             controller : 'maintenanceController',
//             data : { pageTitle: 'Maintenance' },
//             isLogin: true,
//             resolve: {
//                 userProducts: function($http) {
//                     var url = 'api/auctionproducts?lacks_service_type=Maintenance';
//                     //var url = 'api/auctionproducts?has_open_process=False';
//                     //var params = { 'q' :  'maintenance'};
//                     return $http({ 
//                         method: 'GET', 
//                         url: url,
//                         //params:params,
//                     }).then(function(response){
//                         return response.data;
//                     })
//                 }
//             }
            
//         })

//         .state('partsAccessories', {
//             url:'/partsAccessories',
//             templateUrl : 'static/templates/userapp/partsAccessories/partsAccessories.html',
//             //controller : 'logisticsController',
//             isLogin: true
//         })

//         .state('logistics', {
//             url:'/logistics',
//             templateUrl : 'static/templates/userapp/logistics/logistics.html',
//             controller : 'logisticsController',
//             data : { pageTitle: 'Logistics' },
//             isLogin: true,
//             resolve: {
//                 userProducts: function($http) {
//                     var url = 'api/auctionproducts?lacks_service_type=Logistics';
//                     //var params = { 'q' :  'logistics'};
//                     return $http({ 
//                         method: 'GET', 
//                         url: url,
//                         //params:params,
//                     }).then(function(response){
//                         return response.data;
//                     })
//                 }
//             }

//         })

//         .state('serviceRequestThanks', {
//             url: '/serviceRequestThanks',
//             //template : "<h1>Main</h1><p>Click on the links to change this content</p>"
//             templateUrl : 'static/templates/userapp/partials/serviceRequestThanks.html',
//             controller: 'serviceRequestThanksController',
//             isLogin: true
//         })



//         .state('home', {
//             url: '/home',
//             //template : "<h1>Main</h1><p>Click on the links to change this content</p>"
//             templateUrl : 'static/templates/userapp/home/home.html',
//             controller: 'homePageController',
//             data : { pageTitle: 'Hecms | Home' },
//             isLogin: true

//         })

//         .state('howitworks', {
//             url: '/howitworks',
//             //template : "<h1>Main</h1><p>Click on the links to change this content</p>"
//             templateUrl : 'static/templates/userapp/howitworks/howitworks.html',
//             data : { pageTitle: 'How it works' }
//             //controller: 'aosdoas'
//         })

//         .state('login', {
//             //contacts?myParam
//             url:'/{oauth_token}login',
//             data : { pageTitle: 'Hecms | Login' },
//             templateUrl : 'static/templates/userapp/login/login.html',
//             controller : 'signInController'

//         })

//         .state('join', {
//             url: '/join',
//             templateUrl : 'static/templates/userapp/join/join.html',
//             controller : "joinController",
//             data : { pageTitle: 'Hecms | Join' }
//         })

//         .state('forgot-password', {
//             url:'/forgot-password',
//             templateUrl : 'static/templates/userapp/forgotPassword/forgotPassword.html',
//             controller : 'forgotPwdController',
//             data : { pageTitle: 'Forgot Password' }

//         })

//         .state('help', {
//             url:'/help',
//             templateUrl : 'static/templates/userapp/help/help.html'
//             //controller : 'forgotPwdController'

//         })



        //$locationProvider.html5Mode(true);
        $urlRouterProvider.otherwise('/');
         
});


  gaiaApp.config(function(hotkeysProvider) {
    hotkeysProvider.includeCheatSheet = true;
  })

gaiaApp.config([
    '$httpProvider', function( $httpProvider ){
        //var csrftoken = Cookies.get('csrftoken');
        $httpProvider.interceptors.push('tokenAuthInterceptor');
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        //$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        //$httpProvider.defaults.headers.common['X-CSRFToken'] = csrfToken; 
    }
])

gaiaApp.config([
    '$interpolateProvider', function( $interpolateProvider ){
        $interpolateProvider.startSymbol('[[').endSymbol(']]'); 
    }
])



// //ANGULAR EASYFB CONFIGURATIONS


// // gaiaApp.config(function (ezfbProvider) {
// //   var myInitFunction = function ($window, $rootScope, ezfbInitParams) {
// //     $window.FB.init({
// //       appId: '441518596238914',
// //       version: 'v2.8'
// //     });
// //     // or
// //     // $window.FB.init(ezfbInitParams);

// //     $rootScope.$broadcast('FB.init');
// //   };

// //   ezfbProvider.setInitFunction(myInitFunction);
// // });




gaiaApp.run(['$rootScope', '$state', '$stateParams', '$location', '$window', '$uibModal', 'userSessionServices',
    function($rootScope, $state, $stateParams, $location, $window, $uibModal, userSessionServices )
{




//     //CHECK IF USER DATA IS AVAILABLE
//     // if(userSessionServices.isAuthenticated() && !$rootScope.userdata){
//     //     $rootScope.userdata = JSON.parse($window.sessionStorage.getItem('userDataString'));
//     // }


    //RUN CODE WHEN ROUTE CHANGES
    $rootScope.$on('$stateChangeStart', function(event, next, toStateParams){

        var authenticationStatus = userSessionServices.isAuthenticated();

        if(next.isLogin == undefined){

        }
        else if( !authenticationStatus && next.isLogin == true ){ // REDIRECT TO LOGIN IF ATTEMPTING TO ENTER AN AUTHENTICATED URL
            event.preventDefault()
            $rootScope.savedLocation = $location.url;
            $window.location.assign('/#index');;

        }else if(authenticationStatus && next.isLogin!= true  ){// NOT AN AUTHENTICATED URL WITH TOKEN AVAILABLE

            event.preventDefault();

            //IF NO USER DATA IS AVAILABLE GET IT

            if ($window.sessionStorage.getItem('userDataString')){
                $window.location.assign('/#inicio');
                //$location.path('#/home');
                // userSessionServices.userProfile().then(function( userInfo ){
                //     $location.path('home');
                // });    
            }


            $window.location.assign('/#inicio');

        }

        else if( next.isLogin == true && authenticationStatus  ){

            var userDataString = $window.sessionStorage.getItem( 'userDataString' )
            if (!userDataString){
                userSessionServices.userProfile().then(function( userInfo ){
                    $window.sessionStorage.setItem( 'userDataString', JSON.stringify(userInfo) )
                }); 
                // var email = JSON.parse(userDataString).email;
                // if (!email){
                //     var modalInstance = $uibModal.open({
                //         ariaLabelledBy: 'modal-title',
                //         ariaDescribedBy: 'modal-body',
                //         //animation: $scope.animationsEnabled,
                //         templateUrl: '/static/templates/userapp/partials/requestEmail.html',
                //         controller: 'requestEmailModalController',
                //         size: 'md'
                //     });      
                // }
            }
            // else{
            //     userSessionServices.userProfile().then(function( userInfo ){
            //         $window.sessionStorage.setItem( 'userDataString', JSON.stringify(userInfo) )
            //     });   
            // }



        }




        if( authenticationStatus == true){
            $rootScope.userAuthenticated = true;
            $rootScope.brandUrl = '#/inicio';
        }else{
            $rootScope.userAuthenticated = false;
            $rootScope.brandUrl = '#/';
        }

        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;


//     });

//     //RUN FACEBOOK APP PLUGINS
//     $window.fbAsyncInit = function() {
//         FB.init({ 
//           appId: '441518596238914',
//           status: true, 
//           cookie: true, 
//           xfbml: true,
//           version: 'v2.8'
//         })
//         FB.AppEvents.logPageView();

//     };

//     (function(d, s, id){
//      var js, fjs = d.getElementsByTagName(s)[0];
//      if (d.getElementById(id)) {return;}
//      js = d.createElement(s); js.id = id;
//      js.src = "//connect.facebook.net/en_US/sdk.js";
//      fjs.parentNode.insertBefore(js, fjs);
//     }(document, 'script', 'facebook-jssdk'));



//     //GOOGLE API INITIALIZER
//     gapi.load('auth2', function() {//load in the auth2 api's, without it gapi.auth2 will be undefined
//         gapi.auth2.init(
//                 {
//                     client_id: '112766511222-dbe171oatf6lei1b7eff3a2ehia55i30.apps.googleusercontent.com'
//                 }
//         );



    });
}]);
// // // auth2 = gapi.auth2.init(...);

// //     //RUN GOOGLE INITIALIZATION
// //     var auth2 = gapi.auth2.init({
// //         client_id: '112766511222-dbe171oatf6lei1b7eff3a2ehia55i30.apps.googleusercontent.com',
// //         cookiepolicy: 'single_host_origin',
// //         // Request scopes in addition to 'profile' and 'email'
// //         //scope: 'additional_scope'
// //       });
// }]);




// //JAVSCRIPT PROTOTYPE FUNCTIONS
// Date.prototype.addDays = function(days) {
//     this.setDate(this.getDate() + parseInt(days));
//     return this;

// };


// Date.prototype.toISODate= function(){
//     return String(this.getFullYear() + "-" + (this.getMonth() + 1) + "-" + 1);
// }

// Date.prototype.toUTC= function(){
// var now_utc = new Date(this.getUTCFullYear(), this.getUTCMonth(), this.getUTCDate(),  this.getUTCHours(), this.getUTCMinutes(), this.getUTCSeconds());
//     return now_utc;
// }




// Date.prototype.monthDays= function(){
//     var d= new Date(this.getUTCFullYear(), this.getMonth()+1, 0);
//     return d.getDate();
// }

Date.prototype.toISODate= function(){
    return String(this.getFullYear() + "-" + (this.getMonth() + 1) + "-" + 1);
}

Date.prototype.toUTC= function(){
var now_utc = new Date(this.getUTCFullYear(), this.getUTCMonth(), this.getUTCDate(),  this.getUTCHours(), this.getUTCMinutes(), this.getUTCSeconds());
    return now_utc;
}


Number.prototype.formatMoney = function(c, d, t){
var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d == undefined ? "." : d, 
    t = t == undefined ? "," : t, 
    s = n < 0 ? "-" : "", 
    i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))), 
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };