var modalControllers = angular.module('modalControllers',[]);


modalControllers.controller('detallePacienteModalController', function( $scope, $uibModalInstance, paciente ) {
	$scope.paciente = paciente;
	$scope.modelOptions = {
		debounce: {
		  default: 500,
		  blur: 250
		},
	getterSetter: true
	};
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
	$scope.addEstudio= function(){
		console.log('culo')
	}
});

modalControllers.controller('agregar_estudiomodalModalController', function( $scope, $uibModalInstance, paciente, estudios ) {
	$scope.paciente = paciente;

	$scope.estudios = estudios.estudios;
	$scope.clinica_referida_typeahead = estudios.clinicas;
	$scope.medico_referido_typeahead = estudios.medicos;
	$scope.patientFound = true;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
});

modalControllers.controller('addClienteEspecialModalController', function( $scope, $uibModalInstance, $http) {
	//$scope.paciente = paciente;
	$scope.clienteEspecialData = {};
	$scope.clienteEspecialData.nacionalidad = 'J'
	
	// $scope.crearClienteEspecial = function(){
	// 	if($scope.clienteEspecialForm.$valid){
	// 		var url = 'api/clientes_postpago/';
	// 		$http.post(url, $scope.clienteEspecialData).success(function(response){
	// 			$uibModalInstance.close(response); 
	// 		})			
	// 	}

	// }
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
});

modalControllers.controller('detalleFacturaModalController', function( $scope, $uibModalInstance, factura) {
	$scope.factura = factura;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
});

modalControllers.controller('detallesResultadosModalController', function( $scope, $uibModalInstance, resultado) {
	
	$scope.resultado = resultado;
	$scope.codigos = resultado.codigos
	console.log(resultado);

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};



});



modalControllers.controller('notaEstudiosModalController', function( $scope, $uibModalInstance, estudios) {
	$scope.estudios = estudios;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};
});

modalControllers.controller('otroContribuyenteModalController', function( $scope, $uibModalInstance, $http, data, pdfServices ) {

	$scope.facturaForm = {};
	$scope.facturaForm.monto = data.monto.toFixed(2);
	$scope.contribuyente = {};
	$scope.tasa = 0;
	$scope.data = data;
	$scope.facturaForm.nacionalidad = 'J';
	console.log(JSON.stringify(data))

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	$scope.buscarContribuyenteRed = function(){
		$http.post('api/contribuyente/', { id_fiscal : $scope.facturaForm.nacionalidad+$scope.facturaForm.rif }).success(function(contribuyente){
			if (contribuyente){
				console.log(JSON.stringify(contribuyente))
				$scope.facturaForm.razonSocial = contribuyente.nombre;
				$scope.agente_retencion = contribuyente.agente_retencion;
				$scope.contribuyente_IVA = contribuyente.contribuyente_IVA;
				$scope.tasa = contribuyente.tasa;
				
			}else{
				$scope.agente_retencion = 'NO';
				$scope.facturaForm.razonSocial = '';
				$scope.tasa = 0;
			}
		})
	}

	$scope.ImprirFactura = function() {
		if($scope.imprirFacturaForm.$valid){
			$scope.data.is_otro_contribuyente = true;
			$scope.data.otro_rif = $scope.facturaForm.rif;
			$scope.data.otra_razon_social = $scope.facturaForm.razonSocial;
			$scope.data.otra_nacionalidad = $scope.facturaForm.nacionalidad;
			$scope.data.direccion = $scope.facturaForm.direccion;
			var url = 'api/imprimir_estudios/' + String( $scope.data.rif )+'/'+ String( $scope.data.nacionalidad );
			$http.post(url, $scope.data).success(function(response){
    			//PRINT REPORT
			    var client_data = {
			    	nombre: response.nombre,
			    	nro_factura : String(response.id),
			    	direccion : response.direccion,
			    	telefono: String(response.telefono),
			    	fecha : response.created,
			    	total : response.monto

			    };
			    var table_list = [];
			    for(var row in response.detalles){
			    	table_list.push( [ response.detalles[row]['estudio_realizado'], 'Bs.  '+ parseFloat(response.detalles[row]['precio']).formatMoney(2,',','.') ] )
			    }
				pdfServices.facturaNormal(table_list, client_data );
				console.log(JSON.stringify(response))
			})
		}
	}

});

modalControllers.controller('buscarEntreFechasModalController', function( $scope, $uibModalInstance, $http, url ) {

	$scope.url = url;
	$scope.today = function() {
		$scope.dt = new Date();
	};
  	$scope.today();
	$scope.clear = function() {
		$scope.dt = null;
	};

	$scope.dtFrom = new Date();
	$scope.dtTill = new Date();
	$scope.submitSearchBetweenDates = function(){
		var timestamp_gte = $scope.dtFrom;
		var timestamp_lte = $scope.dtTill;
		var url = $scope.url + '?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString();
		$http.get( url ).success(function(response){
	    	$uibModalInstance.close(response); 
		})
	}

	$scope.inlineOptions = {
		customClass: getDayClass,
		minDate: new Date(),
		showWeeks: true
	};

  $scope.dateOptions = {
    dateDisabled: disabled,
    formatYear: 'yy',
    maxDate: new Date(),
    minDate: new Date(),
    startingDay: 1
  };

  // Disable weekend selection
  function disabled(data) {
    var date = data.date,
      mode = data.mode;
    return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
  }

  $scope.toggleMin = function() {
    $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
    $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
  };

  $scope.toggleMin();

  $scope.open1 = function() {
    $scope.popup1.opened = true;
  };

  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };

  $scope.setDate = function(year, month, day) {
    $scope.dt = new Date(year, month, day);
  };

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'ddMMyyyy', 'shortDate'];
  $scope.format = $scope.formats[2];
  //$scope.altInputFormats = ['M!/d!/yyyy'];

  $scope.popup1 = {
    opened: false
  };

  $scope.popup2 = {
    opened: false
  };

  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date();
  afterTomorrow.setDate(tomorrow.getDate() + 1);
  $scope.events = [
    {
      date: tomorrow,
      status: 'full'
    },
    {
      date: afterTomorrow,
      status: 'partially'
    }
  ];

  function getDayClass(data) {
    var date = data.date,
      mode = data.mode;
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i = 0; i < $scope.events.length; i++) {
        var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return $scope.events[i].status;
        }
      }
    }

    return '';
  }

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

});




modalControllers.controller('agregarResultadosModalController', function( $scope, $uibModalInstance, estudios, paciente, $http, Upload, pdfServices ) {

	$scope.resultados_citologias = [];
	$scope.estudios = estudios;
	$scope.paciente = paciente;
	$scope.resultados_citologias = [];
	$scope.regex = '^[0-9]*$';
	
	$scope.llenarResultadoFormData = {};
	$scope.llenarResultadoFormData.estudio_seleccionado = '';


	$scope.ImprimirRes = function(){
		var data = {};
		data.impreso= true;
		var url = 'api/resultados/' + $scope.resultado +'/';
		$http.patch(url, data).success(function(resultado, status){
			if (status ==200){
				var userData = JSON.parse(sessionStorage.getItem('userDataString'))
				var data = {};
				data.nombres = $filter('capfirstlettereachword')(resultado.paciente.nombres); 
				data.doctor =$filter('capfirstlettereachword')(resultado.medico);
				data.edad = $filter('ageFilter')(new Date(resultado.paciente.fecha_nacimiento));
				data.fecha = $filter('date')(new Date(), 'dd-MMMM-yyyy')
				data.centro_referencia = userData.nomina.laboratorio.razon_social;
				data.material_remitido = 'todo'
				pdfServices.resultadosCitologia(resultado.codigos, data );
				for(var i in $scope.estudios){
					if($scope.estudios[i].id == $scope.llenarResultadoFormData.estudio_seleccionado) {
						$scope.estudios.splice( i, 1 );
					}
				}
				$scope.resultados_citologias = [];
				$scope.llenarResultadoFormData.estudio_seleccionado = '';
			}
		})
	}


	$scope.select = function(event, file) {
	    $scope.selectedFile = file;
	}

    $scope.agregarResBiopsia = function(file) {
    	if ($scope.regResultadosForm.$valid){
			var url = 'api/resultados/';
			//console.log($scope.llenarResultadoFormData)
			var data =  {};
			data.estudio = $scope.llenarResultadoFormData.estudio_seleccionado;
			data.adjunto =  file;
			$scope.f = file;
		    file.upload = Upload.upload({
		      url: url,
		      data: data
		    });

		    file.upload.then(function (response) {
				$scope.uploadFields = {};
				$scope.regResultadosForm.$setUntouched();
				$scope.regResultadosForm.$setPristine();
				//$scope.showSuccessMessage = true;
				$scope.selectedFile = undefined;
				alert('Resultado de biopsia registrado');
				$scope.cancel()
				//$scope.f = undefined;

		    }, function (response) {
		      if (response.status > 0)
		        $scope.errorMsg = response.status + ': ' + response.data;
		    	$scope.showSuccessMessage = false;
		    }, function (evt) {
		      // Math.min is to fix IE which reports 200% sometimes
		      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
		    });
		}
    }

	$scope.borrarCodigoCitologia = function( resultado_id ){
		var url = 'api/resultados_codigos/' + resultado_id;
		$http.delete( url ).success( function( response, status ){
			if (status == 202) {
				$scope.resultados_citologias = response;

			}
			
			//$scope.resultados_citologias = response.results[ 0 ].codigos;
		})
	}

	$scope.encontrarResultadosNoImpresos = function(){
		if($scope.llenarResultadoFormData.estudio_seleccionado){
			var url = 'api/estudios_model/' + $scope.llenarResultadoFormData.estudio_seleccionado+'/';
			//PARAMETERS ESTUDIO
			$http.get( url ).success( function( response ){
				$scope.resultados_citologias = response.resultado.codigos||[];
				//console.log(response.resultado.codigos|| [])
				$scope.resultado = response.resultado.id;
			})
		}

	}

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	$scope.registrar = function(){
		if($scope.regResultadosForm.$valid){
			var results_list = []
			for ( var estudio in $scope.estudios){
				var data = {};
				data.estudio = $scope.estudios[estudio].id;
				data.codigos = $scope.estudios[estudio].resultados.split(',');
				results_list.push(data);
			}

			var url ='api/resultados/';
			$http.post(url, results_list).success(function(response){
				console.log(JSON.stringify(response));
			})
		}else{
			return false;
		}


	}


	$scope.agregarResultado= function(){
		if($scope.regResultadosForm.$valid){
			var data = {};
			//data.cedula = $scope.paciente.id;
			data.estudio = $scope.llenarResultadoFormData.estudio_seleccionado;
			//URL NEEDED
			var url ='api/resultados/';
			var tipo_resultado = $scope.estudio_seleccionado_get();
			if(tipo_resultado == 'citologia'){
				data.codigos = $scope.llenarResultadoFormData.resultados;

			}else{
				console.log('biopsia')
			}

			// data.resultados = $scope.resultado;
			$http.post(url, data).success(function(response){
				if(tipo_resultado == 'citologia'){
					//console.log(JSON.stringify(response))
					$scope.llenarResultadoFormData.resultados = '';
					$scope.resultados_citologias = response;
					//$scope.resultados_citologias = response.codigos;
					
				}else{
					console.log(JSON.stringify(response));
				}
				
			})
		}

	}

	$scope.estudio_seleccionado_get = function(){
		for(var estudio in $scope.estudios){
			if ($scope.estudios[estudio].id == $scope.llenarResultadoFormData.estudio_seleccionado){
				return $scope.estudios[estudio].tipo;
			}
		}		
	}

});




modalControllers.controller('estudiosPacienteModalController', function( $scope, $uibModalInstance, estudios, paciente, $http ) {



	$scope.estudios = estudios.results;
	
	$scope.paciente = paciente;

	//PAGINATION
	$scope.itemsPerPage = 10;
	$scope.count = estudios.count;

	$scope.paginationChange = function(){

	    var url = 'api/estudios_realizados/?cedula=' + paciente.cedula+'&page=' + String($scope.currentPage);
	    $http.get(url).success(function(estudios){

			$scope.count = estudios.count
			$scope.estudios = estudios.results;
	    })

	};

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	  $scope.totalItems = 64;
	  $scope.currentPage = 0;

	  $scope.setPage = function (pageNo) {
	    $scope.currentPage = pageNo;
	  };


});
