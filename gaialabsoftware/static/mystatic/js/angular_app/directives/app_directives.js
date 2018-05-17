var appDirectives = angular.module('appDirectives',[]);

appDirectives.directive("elementOnResize", function($window) {
    return {
        restrict: "A",
        scope : {
          'elementOnResize':'&?'
        },
        //require: "ngModel",
         
        link: function(scope, element, attributes, ngModel) {

           scope.width = $window.innerWidth;

           angular.element($window).bind('resize', function(){

            scope.elementOnResize();
            scope.width = $window.innerWidth;
            scope.navCollapsed = true
             // manuall $digest required as resize event
             // is outside of angular
             scope.$digest();
           });

        }
    };
});

appDirectives.directive('panelTable', function($http) {

      var directive = {};
      directive.restrict = 'E';
      //directive.require =  "ngModel";
      directive.transclude= {
          //'labelAddon': '?labelAddon',
          extra: '?extraElement'
      };
      directive.scope = {
          panelTitle : '@',
          searchDateField: "@",
          searchUrl : '@?',
          //maxDate : '=?',
          //tableData : '=?',
          //tableSearch: '=?',
          placeholder :'@?',
          advancedSearch : '&?',
          resultsList: '=?',
          typeAheadModel: '=?'
      };
      //directive.controller = 'orderBookController'
      directive.link = function(scope, element, attributes, ngModel, transclude ) { 
        scope.panelInput = {};
        scope.search = function(){
          var url = scope.searchUrl + scope.panelInput.search;
          $http.get(url).success(function(response ){
            console.log(JSON.stringify(response))
             scope.resultsList = response;
             scope.panelInput.search = '';
          })       
        }
     

      }
      directive.templateUrl = '/static/templates/directive_templates/panel-table.html';
      return directive;
});


appDirectives.directive('maxDateToday', function() {

    var directive = {};
    directive.require =  "ngModel";
    //directive.restrict = '';
    // directive.scope = {
    //   maxDate: '@'
    // };
    directive.scope = false;
    directive.link = function(scope, element, attributes, ngModel) {
             
        ngModel.$validators.maxDateToday = function(modelValue) {
          return modelValue <= new Date();

        };

    }
    return directive;

});  



appDirectives.directive('loading', ['$http', function ($http) {
    return {
        restrict: 'A',
        scope:true,
        link: function (scope, elm, attrs) {
            scope.isLoading = function () {
                return $http.pendingRequests.length > 0;
            };
            scope.$watch(scope.isLoading, function (v) {
                if (v) {
                    elm.css('visibility', 'visible');
                } else {
                    elm.css('visibility', 'hidden');

                }
                //scope.$apply();
            });
        }
    };
}]);


appDirectives.directive('objectsInList', function() {

      var directive = {};
      directive.restrict = 'A';
      //directive.transclude = true;
      // directive.transclude= {
      //     labelAddon: '?labelAddon',
      //     extra: '?extraElement'
      // };

      directive.scope = {
          objectsInList : '='
          //searchDateField: "@",
          // minDate : '=?',
          // maxDate : '=?',
          // tableData : '=?',
          // tableSearch: '=?',
          // placeholder :'@?',
          // advancedSearch : '=?',
          // advSearchFn: '&?',
          // typeAheadModel: '=?'
      };
      //directive.controller = 'orderBookController'
      directive.link = function(scope, element, attributes, ngModel ) { 

        console.log(objectsInList)
            scope.$watch(scope.objectsInList, function (v) {
              console.log(v)
                // if (v) {
                //     elm.css('visibility', 'visible');
                // } else {
                //     elm.css('visibility', 'hidden');

                // }
                //scope.$apply();
            });
        // ngModel.$validators.noResults = function(modelValue) {

        //   return true;

        // };
      }
      //directive.templateUrl = '/static/templates/directive_templates/panel-table.html';
      return directive;
});


appDirectives.directive('tabElement', function($location) {

      var directive = {};
      directive.restrict = 'E';
      directive.scope = {
        'tabList' : '='
      };
      directive.templateUrl = '/static/templates/directive_templates/tabElement.html';
      directive.link = function ( scope, element, attributes, ngModel ) {

          scope.currentUrl = $location.url()
      };
      return directive;
});
