var appServices = angular.module('appServices',[]);



appServices.factory('userSessionServices', ['$http', '$window', '$location', '$q', 
  function( $http, $window, $location, $q ){
    var errors =  {};
    var _identity = undefined, _authenticated = false;
    return{
        logIn : function( credentials ){
            var deferred = $q.defer();
            var url = 'rest-auth/login/';
            $http.post(url, credentials).success(function(token){
              
              if( token!= null ){
                deferred.resolve(token.key);
                $window.sessionStorage.setItem('shoppingCart', '[]')
                $window.sessionStorage.setItem( 'token', token.key );

              }else{
                deferred.reject( 'email/password error' );
              }

            })
            .error( function( error ){
              if( error != null ){
             
                for(var field in error){
                  if(field === 'non_field_errors'){
                    errors[field] = error[field].join(', ')
                  }
                }
      
                  deferred.reject( errors );
                  //deferred.reject('error.non_field_errors[0]');
                //     //errors[field] = error[field].join(', ')
                //   }
                // }
                
              }    

              //deferred.reject(errors);
            })
            return deferred.promise;
            //return(token)? token : false;
        },
        logOut : function(){
            var url = '/rest-auth/logout/'
            $http({
              method: 'POST',
              url: url
            }).then(function (response) {
              if (response.status == 200){
                $window.sessionStorage.clear();
                $location.path('/');         
              }


                // this callback will be called asynchronously
                // when the response is available
              }, function errorCallback(response) {
                console.log(JSON.stringify(response))
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              }); 
        },
        isAuthenticated : function(){
          var token = sessionStorage.getItem('token');
          return(token)? true : false;
        },
        updateSessionStorage : function( newUserDataObj ){
          sessionStorage.setItem('userDataString', JSON.stringify(newUserDataObj));
          return 'success';
          // var token = sessionStorage.getItem('token');
          // return(token)? true : false;
        },
        // getSessionStorage : function( ){
        //   var userDataString = sessionStorage.getItem( 'userDataString')
        //   if( userDataString ){
        //     return JSON.parse( userDataString );
        //   }
        //   return userDataString;
        // },
        userProfile : function()
        {
          var deferred = $q.defer();
          var userDataString = sessionStorage.getItem( 'userDataString');
          if( userDataString ){
            deferred.resolve(JSON.parse( userDataString));
          }else{

            var url = $location.protocol() + "://" + $location.host() + ":" + $location.port() + '/rest-auth/user/';
            $http({
              method: 'GET',
              url: url
            }).then(function successCallback( response ) {
                // $window.sessionStorage.setItem('userDataString', JSON.stringify(response.data[0]));
                // var result = {};
                // result.status = 200;
                deferred.resolve( response.data );
                // this callback will be called asynchronously
                // when the response is available
              }, function errorCallback(error) {
                deferred.resolve(error);
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });

            return deferred.promise;
          }
        }
      }

}]);

 appServices.factory('dateService', function ($window, $q, $uibModal) {

      return {

        yearArray: function(begin, end) {
          //var d = new Date( "01 " + "July 2013");
          var begin = begin.getFullYear();

          //var s = new Date( "01 " + "May 2018");
          var end = end.getFullYear();
          arr = Array();

         for(i = begin; i <= end; i++) arr.push(i);


         return arr;

        },

        searchBetweenDates : function(){
            // var modalInstance = $uibModal.open({
            //     ariaLabelledBy: 'modal-title',
            //     ariaDescribedBy: 'modal-body',
            //     //animation: $scope.animationsEnabled,
            //     templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
            //     controller: 'buscarEntreFechasModalController',
            //     size: 'md'
            //     // resolve: {
            //     //   estudios: function($http){
            //     //       var url = 'api/estudios_realizados?cedula=' + paciente.cedula ;
            //     //       return $http({ 
            //     //           method: 'GET', 
            //     //           url: url
            //     //       }).then(function(estudios){
            //     //           return estudios.data;
            //     //       })
            //     //   }
            //       // paciente:function(){
            //       //     return paciente;
            //       // }
            //    // }

            // });
            // modalInstance.result.then(function (response) {
            //   return response;
            // })
        }

      }
});



 appServices.factory('focus', function($timeout, $window) {
    return function(id) {
      // timeout makes sure that it is invoked after any other event has been triggered.
      // e.g. click events that need to run before the focus or
      // inputs elements that are in a disabled state but are enabled when those events
      // are triggered.
      $timeout(function() {
        var element = $window.document.getElementById(id);
        if(element)
          element.focus();
      });
    };
  });



 appServices.factory('arrayServices', function () {

      return {

        arrayFromObjArray: function(arrayOfObjects, key) {       

          var res = [];
          for (var i in arrayOfObjects){
            res.push(arrayOfObjects[i][key])

          }
          return res;


         },
        findObjectInArray: function(arrayOfObjects, key, value) {       

          for (var i in arrayOfObjects){
            if(arrayOfObjects[i][key] == value){
              return arrayOfObjects[i];
            }
          
          }
          return {};


         }



      }
});


appServices.factory('tokenAuthInterceptor', function ($window, $q, $location) {
    return {
        request: function(config) {

            config.headers = config.headers || {};
            if ($window.sessionStorage.getItem('token')) {
              // may also use localStorage
                config.headers.Authorization = 'Token ' + $window.sessionStorage.getItem('token');
            }
            return config || $q.when(config);
        },
        response: function(response) {
            if (response.status === 401) {
                //  Redirect user to login page / signup Page.
            }
            return response || $q.when(response);
        }
    };
});

appServices.factory('pdfServices', function ( $filter ) {//THIS USES JSPDF LIBRARY
      (function(API){
    API.myText = function(txt, options, x, y) {
        options = options ||{};
        /* Use the options align property to specify desired text alignment
         * Param x will be ignored if desired text alignment is 'center'.
         * Usage of options can easily extend the function to apply different text 
         * styles and sizes 
        */
        if( options.align == "center" ){
            // Get current font size
            var fontSize = this.internal.getFontSize();

            // Get page width
            var pageWidth = this.internal.pageSize.width;

            // Get the actual text's width
            /* You multiply the unit width of your string by your font size and divide
             * by the internal scale factor. The division is necessary
             * for the case where you use units other than 'pt' in the constructor
             * of jsPDF.
            */
            txtWidth = this.getStringUnitWidth(txt)*fontSize/this.internal.scaleFactor;

            // Calculate text's x coordinate
            x = ( pageWidth - txtWidth ) / 2;
        }

        // Draw text at x,y
        this.text(txt,x,y);
    }
    })(jsPDF.API);


    function getCenteredOrigin(doc, txt){
      var fontSize = doc.internal.getFontSize();

      // Get page width
      var pageWidth = doc.internal.pageSize.width;

      // Get the actual text's width
      /* You multiply the unit width of your string by your font size and divide
       * by the internal scale factor. The division is necessary
       * for the case where you use units other than 'pt' in the constructor
       * of jsPDF.
      */
      txtWidth = doc.getStringUnitWidth(txt)*fontSize/doc.internal.scaleFactor;
      // Calculate text's x coordinate
      x = ( pageWidth - txtWidth ) / 2;
      return x          
    }

    return {
        getFontWidth:function(doc, text, unit){
          var width = doc.getStringUnitWidth(text);
          if (typeof unit !='string'){
            throw 'parameter is not a string';
            return false;
          }

           switch(unit) {
              case 'cm':
                  width = 2.54*doc.internal.getFontSize() * width /72
                  break;
              case 'mm':
                  width = 25.4*doc.internal.getFontSize() * width /72
                  break;
              case 'in':
                  width = doc.internal.getFontSize() * width/72
                  break;
              case 'pt':
                  width = doc.internal.getFontSize() * width
                  break;                  
              default:
                  width = doc.internal.getFontSize() * width
          }
          return width;
        } ,
          
        //facturaNormal: function(rows) {},
        facturaNormal: function(rows, client_data) {
          // Default export is a4 paper, portrait, using milimeters for units
          var doc = new jsPDF({
            orientation: 'landscape',
            unit: 'cm', //units
            format: [ 21.5,15.5 ]//paper size
          })




              ////////TEST CODE////  
            //var getColumns = function () {
                // return [
                //     {title: "ID", dataKey: "id"},
                //     {title: "Name", dataKey: "name"},
                //     {title: "Email", dataKey: "email"},
                //     {title: "City", dataKey: "city"},
                //     {title: "Expenses", dataKey: "expenses"}
                // ];
            //};

          var pageContent = function (data) {
            //doc.setFont("courier");
            //HEADER
            //var imgData = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAlgCWAAD/4QEoRXhpZgAATU0AKgAAAAgABQEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAAE7AAIAAAAUAAAAWodpAAQAAAABAAAAbgAAAAAAAACWAAAAAQAAAJYAAAABVElQT0dSQUZJQSBBUklTTUVESQAAC5AAAAcAAAAEMDIyMZADAAIAAAAUAAAA+JAEAAIAAAAUAAABDJEBAAcAAAAEAQIDAJKRAAIAAAADODUAAJKSAAIAAAADODUAAKAAAAcAAAAEMDEwMKABAAMAAAABAAEAAKACAAQAAAABAAAAzKADAAQAAAABAAAAYqQGAAMAAAABAAAAAAAAAAAyMDE3OjA0OjIxIDE2OjM3OjI3ADIwMTc6MDQ6MjEgMTY6Mzc6MjcA/+EKY2h0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8APD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bXA6Q3JlYXRlRGF0ZT0iMjAxNy0wNC0yMVQxNjozNzoyNyIgcGhvdG9zaG9wOkRhdGVDcmVhdGVkPSIyMDE3LTA0LTIxVDE2OjM3OjI3Ij4gPGRjOmNyZWF0b3I+IDxyZGY6U2VxPiA8cmRmOmxpPlRJUE9HUkFGSUEgQVJJU01FREk8L3JkZjpsaT4gPC9yZGY6U2VxPiA8L2RjOmNyZWF0b3I+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDw/eHBhY2tldCBlbmQ9InciPz4A/+0AkFBob3Rvc2hvcCAzLjAAOEJJTQQEAAAAAABXHAFaAAMbJUccAgAAAgACHAI/AAYxNjM3MjccAj4ACDIwMTcwNDIxHAJQABNUSVBPR1JBRklBIEFSSVNNRURJHAI3AAgyMDE3MDQyMRwCPAAGMTYzNzI3ADhCSU0EJQAAAAAAEM49IUfqW2u4sba1qXfq+Gr/wAARCABiAMwDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9sAQwACAgICAgIDAgIDBQMDAwUGBQUF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';
            //doc.addImage(imgData, 'JPEG', 1, 0.5, 4, 2.25);
            doc.setFontType("bold");
            //doc.setFontSize(15);
            //doc.myText("SP Unidad de Diagnóstico Histológico, C.A.",{align: "center"},0,1);
            doc.setFontSize(11);
            //TOTAL
            doc.text('Total:', 17.5, 1.5);

            doc.text('Bs. ' + parseFloat(client_data.total).formatMoney(2,',','.') , 17.5, 2);
            //doc.text('FORMA LIBRE', 17.5, 2.5);
            doc.setLineWidth(0.02);

            //FOOTER
            //doc.myText('Laboradorio de Anatomia Patologica RIF: J-08014181-4',{align: "center"},0,1.5);
            doc.setFontSize(9);
            doc.setFontType("normal");
            //doc.myText('Avenida 5 de Julio, frente a la Policlina Puerto la Cruz, Centro Profesional S.P.,',{align: "center"},0,2);
            //doc.myText('Planta Baja, Puerto La Cruz, Anzoátegui-Teléfonos: (0281) 267 50 45 / 267 38 57',{align: "center"},0,2.5);
            //doc.text('Blanca: ORIGINAL - Copia: SIN DERECHO A CRÉDITO FISCAL', 1, 13.6)

            doc.line(1, 13.7, 20.5, 13.7); // horizontal line bottom

            doc.line(1,2,1,2)

            //RECTANGLE
            doc.rect(1,7.25,19.5,6)
            doc.rect(1,7.25,19.5,6)
            //vertical rect
            doc.rect(16.4,6.5,4.1,6.75)
            doc.rect(1,3,19.5,3)

            doc.setFontSize(8);
            doc.setFontType("bold");
            doc.text('Domicilio Fiscal:', 1.25, 4.25);
            doc.text('Fecha:', 1.25, 5);
            doc.text('Nombre o Razon Social:', 1.25, 3.5);
            doc.text('Telefono:', 1.25, 5.75);
            doc.setFontType("normal");
            doc.text(client_data.nombre, 4.75, 3.5);
            doc.line(1, 3.75, 20.5, 3.75);
            doc.text(client_data.direccion, 3.75, 4.25);
            doc.text($filter('date')(client_data.fecha,'dd/MM/yyyy'), 3, 5);
            doc.line(1, 4.5, 20.5, 4.5);
            doc.text(client_data.telefono, 2.75, 5.75);
            doc.line(1, 5.25, 20.5, 5.25);
            //doc.line(1, 13.7, 20.5, 13.7);

            doc.setFontType("bold");
            doc.setFontSize(7);
            //doc.text('IMPRESO POR: TIPOGRAFÍA ARISMENDI, C.A.', 1, 14);
            doc.setFontType("normal");
            //doc.text('-RIF: J-31361229-4 - Calle Arismendi Nº 43, Puerto La Cruz', 6.5, 14);
            //doc.text('Telefonos:  ( 0281 )  269.95.16   /   266.07.82   -  Nº   Providencia SENIAT/07/00397   de   Fecha   28/02/2008', 1, 14.25);
            //doc.text('Control desde el Nº 00-048301 hasta el Nº 00-049800 - Fecha de Impresion: 24/04/2017 -Región Nor-Oriental', 1, 14.5);
            doc.setFontSize(11);
            doc.setFontType("bold");
            //doc.text('Nº DE CONTROL 00-', 13.5, 14.5);
            doc.text(client_data.nro_factura, 17.25, 14.5);
          
          };

        /////////////////
          var columns = ["Descripcion", 'TOTAL'];

          doc.autoTable(columns, rows,{
                theme: 'plain', // 'striped', 'grid' or 'plain'
                //startY:3,
                margin : {top: 6.5, right: 1, bottom: 2, left: 1},
                headerStyles: {
                  fontStyle: 'bold',
                    lineWidth: 0.02,

                    //lineColor: [34, 34, 34],
                    halign: 'center'
                },
                columnStyles: {
                    0: {columnWidth: 15.4, overflow: 'ellipsize'},
                    1: {columnWidth: 4.1},
                    //2: {columnWidth: 80},
                    // etc
                },
                bodyStyles: {
                  //lineWidth: 0.01,
              //styles: {
                fontStyle: 'normal',
                fontSize: 10,
                font: "helvetica",
                columnWidth: 'auto',
                //lineColor: [34, 34, 34],
                fillColor:false,
                textColor: [34, 34, 34],
                halign: 'center'
                },
              //tableWidth: 'auto', // 'auto', 'wrap' or a number,
              styles: {
                //lineColor: [34, 34, 34],
               // fontStyle: 'normal',
               // fontSize: 10,
               // font: "helvetica",
               // columnWidth: 'auto',
               // fillColor:false,
               // textColor: 20

              },
              showHeader: 'everyPage', // 'everyPage', 'firstPage', 'never',
                // Hooks
                createdHeaderCell: function (cell, data) {},
                createdCell: function (cell, data) {},
                drawHeaderRow: function (row, data) {},
                drawRow: function (row, data) {},
                drawHeaderCell: function (cell, data) {},
                drawCell: function (cell, data) {},
                addPageContent: pageContent
              });
            //doc.text('Hello world!', 10, 10)
            //doc.save('a4.pdf')
            //doc.output('dataurlnewwindow'); 
            doc.autoPrint();
            window.open(doc.output('bloburl'), '_blank');
        },
        
        resultadosCitologia: function(citologia, datos_cliente) {
          // Default export is a4 paper, portrait, using milimeters for units
          var y;
          var x;
          var lineSpacing = 0.5;
          var title_length;
          var doc = new jsPDF({
            orientation: 'portrait',
            unit: 'cm', //units
            format: [ 21.6, 27.8 ]//paper size
          })
          doc.setFont("courier");
            //doc.setFontType("bold");
            //doc.setFontSize(15);
            //doc.myText("SP Unidad de Diagnóstico Histológico, C.A.",{align: "center"},0,1);
            doc.setFontSize(10);

            //NOMBRE
            var text = 'NOMBRE:';
            x = 2;
            y = 7;
            doc.text(text, x, y);
            title_length =this.getFontWidth(doc,text,'cm' );
            doc.text(datos_cliente.nombres, x+title_length+0.1, y);

            //ORDEN:
            text = 'ORDEN:';
            y = y+lineSpacing;
            doc.text(text, 2, y);
            title_length =this.getFontWidth(doc,text, 'cm');
            doc.text(datos_cliente.doctor, 2+title_length+0.1, y);

            //EDAD:
            text = 'EDAD:';
            x = 15;
            y = 7;
            doc.text(text, x, y);
            title_length =this.getFontWidth(doc,text, 'cm');
            doc.text(String(datos_cliente.edad), x+title_length+0.1, y);


            //FECHA:
            text = 'FECHA:';
            x = 15;
            y = y+lineSpacing;
            doc.text(text, x, y);
            title_length =this.getFontWidth(doc,text, 'cm');
            doc.text(datos_cliente.fecha, x+title_length+0.1, y);



            //CENTRO DE REFERENCIA:
            text = 'CENTRO DE REFERENCIA:';
            x = 2;
            y = y+lineSpacing;
            doc.text(text, x, y);
            title_length =this.getFontWidth(doc,text,'cm' );
            doc.text(datos_cliente.centro_referencia, x+title_length+0.1, y);


            //MATERIAL REMITIDO:
            text = 'MATERIAL REMITIDO:';
            x = 2;
            y = 11;
            doc.text(text, x, y);
            title_length =this.getFontWidth(doc,text,'cm' );
            doc.text(datos_cliente.material_remitido, x+title_length+0.1, y);

            //doc.setFontType("normal");
            var y = 15
            for (var fila in citologia){
              var titulo = citologia[fila]['codigo']['titulo'];
              if(titulo){
                //doc.text(citologia[fila]['codigo']['descripcion'], 2, y);
                doc.myText(citologia[fila]['codigo']['descripcion'],{align: "center"},2,y);
                //UNDERLINE TEXT
                var font_width = this.getFontWidth(doc,citologia[fila]['codigo']['descripcion'], 'cm')
                doc.myText(citologia[fila]['codigo']['descripcion'],{align: "center"},2,y);

                var origin =getCenteredOrigin(doc, citologia[fila]['codigo']['descripcion'])
                doc.setLineWidth(0.01);
                doc.line(origin, y+0.2, origin+font_width, y+0.2);
                //doc.line(origin, y+0.4, origin+font_width, y+0.4);
                y=y+0.3
              }else{

                doc.text(citologia[fila]['codigo']['descripcion'], 2, y);
              }
              y=y+lineSpacing
            }

            //doc.output('dataurlnewwindow');
            doc.autoPrint();
            window.open(doc.output('bloburl'), '_blank');
            //doc.save('a4.pdf')
        },
        reporteDiario: function(reporte) {
          // Default export is a4 paper, portrait, using milimeters for units
          var y;
          var x;
          var lineSpacing = 0.7;
          var title_length;
          var doc = new jsPDF({
            orientation: 'portrait',
            unit: 'cm', //units
            format: [ 21.6, 27.8 ]//paper size
          })
          doc.setFont("courier");
            doc.setFontType("bold");
            doc.setFontType("underline");
            doc.setFontSize(17);
            doc.myText("SP Unidad de Diagnóstico Histológico, C.A.",{align: "center"},0,1);
            doc.myText("Reporte diario",{align: "center"},0,2);

            doc.setFontType("normal");
            doc.setFontSize(14);

            //NOMBRE
            var text = 'FECHA:';
            x = 2;
            y = 3;
            doc.text(text, x, y);
            title_length =this.getFontWidth(doc,text,'cm' );
            doc.text($filter('date')(reporte.day, 'dd MMMM yyyy'), x+title_length+0.1, y);

            //ORDEN:
            text = 'MONTO:';
            y = y+lineSpacing;
            doc.text(text, 2, y);
            title_length =this.getFontWidth(doc,text, 'cm');
            doc.text('Bs. '+$filter('number')(reporte.monto,  '2'), 2+title_length+0.1, y);

            //ORDEN:
            text = 'Cantidad:';
            y = y+lineSpacing;
            doc.text(text, 2, y);
            title_length =this.getFontWidth(doc,text, 'cm');
            doc.text(String(reporte.c), 2+title_length+0.1, y);


            // //FECHA:
            // text = 'FECHA:';
            // x = 15;
            // y = y+lineSpacing;
            // doc.text(text, x, y);
            // title_length =this.getFontWidth(doc,text, 'cm');
            // doc.text(datos_cliente.fecha, x+title_length+0.1, y);



            // //CENTRO DE REFERENCIA:
            // text = 'CENTRO DE REFERENCIA:';
            // x = 2;
            // y = y+lineSpacing;
            // doc.text(text, x, y);
            // title_length =this.getFontWidth(doc,text,'cm' );
            // doc.text(datos_cliente.centro_referencia, x+title_length+0.1, y);


            // //MATERIAL REMITIDO:
            // text = 'MATERIAL REMITIDO:';
            // x = 2;
            // y = 11;
            // doc.text(text, x, y);
            // title_length =this.getFontWidth(doc,text,'cm' );
            // doc.text(datos_cliente.material_remitido, x+title_length+0.1, y);

            // //doc.setFontType("normal");
            // var y = 15
            // for (var fila in citologia){
            //   var titulo = citologia[fila]['codigo']['titulo'];
            //   if(titulo){
            //     //doc.text(citologia[fila]['codigo']['descripcion'], 2, y);
            //     doc.myText(citologia[fila]['codigo']['descripcion'],{align: "center"},2,y);
            //     //UNDERLINE TEXT
            //     var font_width = this.getFontWidth(doc,citologia[fila]['codigo']['descripcion'], 'cm')
            //     doc.myText(citologia[fila]['codigo']['descripcion'],{align: "center"},2,y);

            //     var origin =getCenteredOrigin(doc, citologia[fila]['codigo']['descripcion'])
            //     doc.setLineWidth(0.01);
            //     doc.line(origin, y+0.2, origin+font_width, y+0.2);
            //     //doc.line(origin, y+0.4, origin+font_width, y+0.4);
            //     y=y+0.3
            //   }else{

            //     doc.text(citologia[fila]['codigo']['descripcion'], 2, y);
            //   }
            //   y=y+lineSpacing
            // }

            //doc.output('dataurlnewwindow');
            //doc.autoPrint();
            window.open(doc.output('bloburl'), '_blank');
            //doc.save('a4.pdf')
        }



    };
});

