var appControllers = angular.module('appControllers',['modalControllers']);

 	appControllers.controller('pacientePostPagoController', [ '$scope', 'estudios', 'hotkeys','$http','uibDateParser','arrayServices','$uibModal',function( $scope, estudios, hotkeys, $http, uibDateParser,arrayServices, $uibModal ){

	$scope.clinica_referida_typeahead = estudios.clinicas;
	$scope.medico_referido_typeahead = estudios.medicos;
	$scope.clientesPostPago = estudios['clientes_postpago'];
	$scope.formData = {};
	$scope.formData.patron = '';
	$scope.estudioData = {};
	$scope.formData.nacionalidad = 'V';
	
	$scope.format = 'ddMMyyyy';
	$scope.estudios = estudios.estudios;
	$scope.selectAll = false;
	$scope.subPruebaTypeahead = [];

	$scope.finanzas = {};
	$scope.finanzas.descuento = 0;
	$scope.displayDiscount = false;

	$scope.form_editable = true;
	$scope.patientFound = false;
	$scope.patch_method = false;

	$scope.generarNotaEstudio= function(){
    	var data = {}
    	data.estudios = arrayServices.arrayFromObjArray($scope.estudiosAgregados, 'id');
    	data.monto = $scope.totalEstudios();
    	data.descuento = $scope.finanzas.descuento;
    	data.rif = $scope.formData.cedula;
    	data.nombre = $scope.formData.nombres;
    	data.direccion = $scope.formData.direccion;
    	data.nacionalidad = $scope.formData.nacionalidad;
    	data.telefono = $scope.formData.celular;

	    var url = 'api/generar_nota_postpago/' + String( $scope.formData.cedula )+'/'+ String( $scope.formData.nacionalidad );
		$http.post(url, data).success(function(response, status){
    		if (status == 200){

    			$scope.estudiosAgregados = [];
    			$scope.finanzas.descuento = 0;

	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/notaEstudiosModal.html',
	            controller: 'notaEstudiosModalController',
	            size: 'lg',
	            resolve: {
					estudios: function( $http ){
						return response;
					}
	            }
	        });

    		}
		})
	}



	$scope.pacienteTabList = [
		//{ url : 'auctionproducts', name : 'Register Purchases'  },
		{ url : 'inicio', name : 'Paciente Normal'  },
		{ url : 'paciente_post_pago', name : 'Paciente Post Pago'  }
		//{ url : 'orderhistory', name : 'Order History'  },
		//{ url : 'paymenthistory', name : 'Payment History'  }
		//{ url : 'paymenthistory', name : 'Payment History'  }
	] 

	document.getElementById('cedula').focus();

	$scope.toggleDiscount = function(){
		$scope.displayDiscount = !$scope.displayDiscount;
		if ($scope.displayDiscount == false){
			$scope.finanzas.descuento = 0;
		}
	}

	$scope.fillSubPrueba = function(){
		if( $scope.estudioData.prueba){
			$scope.estudioData.estudio_realizado = '';
			for (var estudio in $scope.estudios){
				if ( $scope.estudios[ estudio ].id  == $scope.estudioData.prueba.id ){
					$scope.subPruebaTypeahead=$scope.estudioData.prueba.sub_tipos_estudios
					//$scope.subPruebaTypeahead= arrayServices.arrayFromObjArray($scope.estudios[ estudio ].sub_tipos_estudios, 'nombre')
					//$scope.subprueba_list = $scope.estudios[ estudio ]['sub_tipos_estudios'];
					break;
					//$scope.subPruebaTypeahead = $scope.estudios[ estudio ].sub_tipos_estudios;
				}else{
					$scope.subprueba_list = [];
				}
				// else if( $scope.estudios[ estudio ].nombre  == 'biopsia' ){
				// 	console.log(arrayServices.arrayFromObjArray($scope.estudios[ estudio ].sub_tipos_estudios, 'nombre'))
				// 	//$scope.subPruebaTypeahead = $scope.estudios[ estudio ].sub_tipos_estudios;
				// }
			}		
		}
	}


	$scope.agregarResultados = function( paciente ){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/agregarResultadosModal.html',
	            controller: 'agregarResultadosModalController',
	            size: 'lg',
	            resolve: {
					estudios: function( $http ){
					    //var url = 'api/estudios_realizados/?cedula=' + paciente.cedula +'&results_printed=False&impreso=True';
					    var url = 'api/estudios_model/?cedula='+ paciente.cedula +'&impreso=True&results_printed=False';
					    return $http({ 
					        method: 'GET', 
					        url: url
					    }).then(function(estudios){
					    	if(estudios.data.length ==0){
					    		alert('Paciente no tiene estudios pendientes')
					    		throw true;
					    	}
					        return estudios.data;
					    })
					},
					paciente: function(){
						return paciente
					}
					// estudios: function( $http ){
					//     var url = 'api/estudios_realizados/?cedula=' + paciente.cedula +'&results_printed=False&impreso=True';
					//     return $http({ 
					//         method: 'GET', 
					//         url: url
					//     }).then(function(estudios){
					//     	if(estudios.data.results.length ==0){
					//     		alert('Paciente no tiene estudios pendientes')
					//     		throw true;
					//     	}
					//         return estudios.data;
					//     })
					// },
					// paciente: function(){
					// 	return paciente
					// }
	            }
	        });

	}

	$scope.selectAllchx = function(){
		//$scope.selectAll = !$scope.selectAll;
		for (var i in $scope.estudiosAgregados){
			//if($scope.estudiosAgregados[i].services.services_present == false){
				$scope.estudiosAgregados[i].checked = $scope.selectAll;
			//}
	
		}
	}

	$scope.modelOptions = {
		debounce: {
		  default: 500,
		  blur: 250
		},
	getterSetter: true
	};

	hotkeys.bindTo($scope)
	.add({
	  combo: 'ctrl+1',
	  description: 'Para agregar examenes a cliente',
	  allowIn: ['INPUT', 'SELECT', 'TEXTAREA'],
	  callback: function() {
	  	$scope.agregarExamen()
	  }
	})
    // you can chain these methods for ease of use:
    //.add ({...});

    $scope.borrarExamenesSelecionados = function(){
    	if ($scope.estudiosAgregados.length>0){

			var del_list = [];
			for (var row in $scope.estudiosAgregados){
				if ($scope.estudiosAgregados[row].checked == true ){
					del_list.push($scope.estudiosAgregados[row].id)
				}
			}
			if (del_list.length == 0){
				alert('No ha seleccionado examenes de la lista');
				return false;
			}


			var delete_answer =  confirm("¿Esta seguro(a) de que desea borrar los estudios seleccionados?");


			if (delete_answer){
				var url = 'api/deleteunprinted/?cedula=' + String($scope.formData.cedula)+ '&impreso=False';
				var data = {}
				data.del_list  = del_list;
				$http.post(url, data).success(function(response, status){
					if(status == 200){
						$scope.estudiosAgregados = response.sub_tipos_estudios;
						alert('Ha borrado los estudios exitosamente');
					}
				})
				.error(function(errors, status){
					console.log(status);
				})
			}else{
				return false;
			}

    	}else{
    		return false;
    	}

    }


    $scope.totalEstudios = function(){
    	var total = 0;
    	if($scope.estudiosAgregados){
			for (var i in $scope.estudiosAgregados){
				total += parseFloat($scope.estudiosAgregados[i].precio)
				
			}
			return total - (total * $scope.finanzas.descuento)/100;
    	}
    	return 0;
    	
    }


    $scope.addEstudio = function(){

    	if ($scope.addPruebaForm.$valid){
    		var url = 'api/paciente_post_pago/';
    		//var data = $scope.estudioData;
    		var data = {};
    		data.paciente = $scope.formData.cedula;
    		data.estudio_realizado = arrayServices.findObjectInArray($scope.subPruebaTypeahead, 'nombre', $scope.estudioData.estudio_realizado).id
    		console.log(data.estudio_realizado)
    		data.medico = $scope.estudioData.medico;
    		data.clinica = $scope.estudioData.clinica;
    		data.patron = $scope.formData.patron;
    		$http.post(url, data).success(function(response){
				//$scope.clinica_referida_typeahead.push(clinica);
				//$scope.medico_referido_typeahead.push(medico);
				console.log(JSON.stringify(response))
    			$scope.estudiosAgregados = response.sub_tipos_estudios;
    			$scope.estudioData = {};
				$scope.addPruebaForm.$setUntouched();
				$scope.addPruebaForm.$setPristine();
    			//$scope.examenesAgregados = response;
    		})
    	}

    }


		$scope.ingresarPaciente= function(){
			if( $scope.ingresoPacienteForm.$valid ){
				var url = 'api/pacientes_post_pago/';
				if( $scope.patch_method == true ){
					url = url + String( $scope.formData.cedula ) + '/';
					$http.patch( url, $scope.formData ).success( function( response, status ){
						if( status == 200 ){
							//$scope.formData = {};
							//$scope.formData.nacionalidad = 'V';
							$scope.ingresoPacienteForm.$setUntouched();
							$scope.ingresoPacienteForm.$setPristine();
							$scope.patientFound = true;
							$scope.form_editable = false;
							alert( 'Datos de paciente modificados' );
							document.getElementById( 'medico_referido' ).focus();
							$scope.patch_method = false;
							$scope.showCancelarEdicion = false;
						}
					})	
				}else{
					$http.post(url, $scope.formData).success(function( response, status ){
						if( status == 200 ){
							//$scope.formData = {};
							//$scope.formData.nacionalidad = 'V';
							$scope.patientFound = true;
							$scope.patch_method = true;
							$scope.form_editable = false;
							$scope.formData.id  = response.id;
							$scope.ingresoPacienteForm.$setUntouched();
							$scope.ingresoPacienteForm.$setPristine();
							alert('Paciente Registrado');
							document.getElementById('medico_referido').focus();

							$scope.patientFound = true;
						}
					})				
				}
				

			}
		}


		$scope.cancelarEdicion= function(){
			//$scope.patientFound = true;
			//$scope.showCancelarEdicion = false;
			$scope.patch_method = false;
			$scope.form_editable  = false;
		}

		$scope.editPatient = function(){
			//$scope.patientFound = false;
			$scope.patch_method = true;
			$scope.form_editable = true;
		}

		$scope.findPatient = function(){
			if( $scope.ingresoPacienteForm.cedula.$valid ){
				$scope.patientFound = false;
				var nacionalidad_temp = $scope.formData.nacionalidad;
				var cedula_temp = $scope.formData.cedula;
				$scope.formData = {
					nacionalidad : nacionalidad_temp,
					cedula : cedula_temp
				};
				var url = 'api/verify_post_pago_patient/';
				var params = {};
				params.nacionalidad = $scope.formData.nacionalidad;
				params.cedula = $scope.formData.cedula;
				$http.post( url, params ).success( function( response, status ){
					if (status == 203){
						$scope.patientFound = false;
						$scope.form_editable = true;
						$scope.patch_method = false;
						$scope.formData.nombres = response.nombres;
						$scope.formData.apellidos = response.apellidos;
						document.getElementById('fecha_nacimiento').focus();
					}else if(status== 204){
						$scope.patientFound = false;
						$scope.form_editable = true;
						$scope.patch_method = false;
						document.getElementById('nombres').focus();
						return false;
					}else if(status== 200){
						response.fecha_nacimiento = uibDateParser.parse(response.fecha_nacimiento, 'yyyy-MM-dd');
						response.cedula  = parseInt(response.cedula);
						$scope.formData = response;
						$scope.formData.patron = String(response.patron);
						$scope.patientFound = true;
						$scope.form_editable = false;
						$scope.patch_method = false;
						$scope.estudiosAgregados = response.sub_tipos_estudios;
						document.getElementById('medico_referido').focus();
					}

				})
				//alert('if patient exists find user profile otherwise, leave fields blank')			
			}

		}

		// $scope.agregarExamen = function(){
	 //        var modalInstance = $uibModal.open({
	 //            ariaLabelledBy: 'modal-title',
	 //            ariaDescribedBy: 'modal-body',
	 //            animation: $scope.animationsEnabled,
	 //            templateUrl: 'static/templates/modals/addTestModal.html',
	 //            controller: 'agregarExamenController',
	 //            size: 'sm'
	 //            // resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
	 //            //   minDate: function(){
	 //            //     return $scope.minDate;
	 //            //   },
	 //            //   maxDate: function(){
	 //            //     return $scope.maxDate;
	 //            //   },
	 //            //    fechaEgreso: function(){
	 //            //     return $scope.fechaEgreso;
	 //            //   }    
	 //            // }
	 //        });
	
	}])

 	appControllers.controller('estadisticasController', [ '$scope', function( $scope ){

	}])


 	appControllers.controller('reportesController', [ '$scope', 'context','pdfServices', '$http',function( $scope, context, pdfServices, $http ){
 		$scope.reportes= context.reportes;
 		$scope.reportesData = {};
 		$scope.reportesData.dt = new Date().toUTC();
		$scope.maxDate = new Date(context.maxDate).toUTC();
		$scope.minDate = new Date(context.minDate).toUTC();

		$scope.queryDate = function(){
			var url = 'api/reportes/' + $scope.reportesData.dt.toISOString();
			$http.get(url).success(function(context){
				$scope.reportes = context.reportes;
			})
		}

 		$scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
 		$scope.format = $scope.formats[0];
		$scope.open1 = function() {
			$scope.popup1.opened = true;
		};
		$scope.popup1 = {
			opened: false
		};

		$scope.dateOptions = {
			minMode: 'month',
			maxDate: $scope.maxDate,
			minDate: $scope.minDate
		};


		$scope.refresh = function(){
			$scope.reportes = reportes;
		}
 		$scope.printReport= function(report){
 			pdfServices.reporteDiario(report)
 			console.log(report)
 		}
	}])	


 	appControllers.controller('indexController', [ '$scope', 'userSessionServices', '$location', 'context',function( $scope, userSessionServices, $location, context ){

 		$scope.loginFormData = {};
 		console.log(context)
 		$scope.context = context
		$scope.loginPost = function(){

			if($scope.loginForm.$valid){

		        userSessionServices.logIn( $scope.loginFormData )

			        .then(function( token ){
			        	userSessionServices.userProfile().then(function( response ){
			        		sessionStorage.setItem( 'userDataString', JSON.stringify( response ) );
			        		$location.path('inicio');
			        		// if(response.status == 200){
			        		// 	$location.path('/home');
			        		// }
			        		
			        	});
			        	

			        }).catch(function(errors){
			        	console.log(JSON.stringify(errors))
			        	$scope.errors = errors
			        })

			}

		}
	}])

	//}])

 	appControllers.controller('estudiosController', ['$scope', 'listaEstudios', '$uibModal', '$http',function( $scope, listaEstudios, $uibModal, $http ){
 		
 		console.log(listaEstudios)
 		$scope.listaEstudios = listaEstudios;
 		$scope.transclusion = {};
		$scope.transclusion.dateRange = 'last30';
		$scope.resultsFor = '';

		// $scope.searchBackend = function(){
		// 	var url = 'api/estudios_model/?search=' + $scope.searchParam;
		// 	$http.get(url).success(function(response ){
		// 		console.log(response)
		// 		//if(response.length > 0){
		// 			//$scope.results = '0 Results Found;'
		// 			$scope.resultsFor = $scope.searchParam;
		// 			$scope.searchParam = '';
		// 			$scope.listaEstudios = response;
		// 		//}
		// 			$scope.resultados = response.length;
		// 	})	
		// }

 		$scope.mostrarDetallesPaciente = function(paciente){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/detallePacienteModal.html',
	            controller: 'detallePacienteModalController',
	            size: 'md',
	            resolve: {
	              paciente: function(){
	                return paciente;
	              }  
	            }
	        });
 		}


		$scope.refreshList = function(){
			$scope.listaEstudios = listaEstudios;
			$scope.resultados = 0;
			$scope.transclusion.dateRange = 'last30';
			$scope.resultsFor = '';
		}

		$scope.queryDate = function(dateRange){

			switch(dateRange) {

			    case 'last30':
			    	var now_date = new Date()
			    	var timestamp_lte = new Date();
			        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
			        break;

			    case 'months-6':
			    	var now_date = new Date()
			    	var timestamp_lte = new Date();
			        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
			        break;

			    default:
			    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
			        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
			} 


			var url = 'api/estudios_model/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
			$http.get(url).success(function(response ){

					$scope.resultados = response.length;
					$scope.listaPacientes = response;
					function selectOptionText(){
						if($scope.transclusion.dateRange == 'last30'){
							return 'Ultimos 30 dias';
						}else if($scope.transclusion.dateRange == 'months-6'){
							return 'Ultimos 6 meses';
						}else{
							return $scope.transclusion.dateRange;
						}
					}

					$scope.resultsFor = selectOptionText();
					
				
			})	
		
		}



 		$scope.totalPrecio = function(){
 			var total_precio = 0;
 			for(var estudio in $scope.listaEstudios){
 				total_precio +=parseFloat($scope.listaEstudios[estudio].estudio_realizado.precio);
 			}
 			return total_precio;
 		}

 		$scope.filtrarEntreFechasModal = function(url){

            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
                controller: 'buscarEntreFechasModalController',
                size: 'md',
                resolve: {
                  url: function(){
					return url;
                  }

                }
            });
            modalInstance.result.then(function (listaEstudios) {
				//if(listaEstudios.length > 0){
					//$scope.results = '0 Results Found;'
					$scope.resultsFor = $scope.searchParam;
					$scope.searchParam = '';
					$scope.listaEstudios = listaEstudios;
					$scope.resultados = listaEstudios.length;
				//}
				//$scope.resultados = 0;
            })
 		}

	}])


 	appControllers.controller('facturasController', ['$scope', 'listaFacturas','pdfServices','$uibModal','$http',function( $scope, listaFacturas, pdfServices, $uibModal, $http ){
 		
 		$scope.listaFacturas = listaFacturas;
 		$scope.transclusion = {};
		$scope.transclusion.dateRange = 'last30';
		$scope.resultsFor = '';

 		$scope.filtrarEntreFechasModal = function(url){
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
                controller: 'buscarEntreFechasModalController',
                size: 'md',
                resolve: {
                  url: function(){
					return url;
                  }

                }
            });
            modalInstance.result.then(function (listaFacturas) {
				$scope.resultsFor = $scope.searchParam;
				$scope.searchParam = '';
				$scope.listaFacturas = listaFacturas;
				$scope.resultados = listaFacturas.length;

            })
 		}

		$scope.verFactura = function( response ){
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
			pdfServices.facturaNormal(table_list, client_data);
		}
		$scope.detallesFactura = function(factura){
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/detalleFactura.html',
                controller: 'detalleFacturaModalController',
                size: 'md',
                resolve: {
                  factura: function(){
					return factura;
                  }

                }
            });
		}

		$scope.refreshList = function(){
			$scope.listaFacturas = listaFacturas;
			$scope.resultados = 0;
			$scope.transclusion.dateRange = 'last30';
			$scope.resultsFor = '';
		}


	}])

 	appControllers.controller('postPagoController', ['$scope', 'clientesPostPago', '$http', '$uibModal',function( $scope, clientesPostPago, $http, $uibModal ){
 		$scope.clientesPostPago = clientesPostPago;	
 		$scope.resultsFor = '';
 		$scope.transclusion = {}

		$scope.transclusion.dateRange = 'last30';

		$scope.lengthTable = function(){
			console.log($scope.clientesPostPago.length>0)
			return $scope.clientesPostPago.length>0;
		}

		$scope.postPagoSelected = function(){
			if($scope.cliente){
				var url = 'api/pacientes/?patron='+$scope.cliente;
				$http.get(url).success(function(pacientes){
					$scope.pacientes = pacientes;
					//$scope.lengthTable()
				})
			}
		}

		$scope.datosPersonales = function(paciente){
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/detallePacienteModal.html',
                controller: 'detallePacienteModalController',
                size: 'md',
                resolve: {
                  paciente: function(){
					return paciente;
                  }

                }
            });		
		}

		$scope.getEstudios = function(paciente){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/estudiosPacienteModal.html',
	            controller: 'estudiosPacienteModalController',
	            size: 'md',
	            resolve: {
					estudios: function($http){
					    var url = 'api/estudios_realizados/?cedula=' + paciente.cedula+'&impreso=True';
					    return $http({ 
					        method: 'GET', 
					        url: url
					    }).then(function(estudios){
					        return estudios.data;
					    })
					},
					paciente:function(){
							return paciente;
					}
	            }
	        });		
		}


		$scope.searchBackend = function(){



			//var url = 'api/pacientes/?impreso=True&search_param=' + $scope.searchParam;
			var url = 'api/pacientes/?patron='+$scope.cliente+'&search='+$scope.searchParam;
			$http.get(url).success(function(response ){
				//if(response.length > 0){
					//$scope.results = '0 Results Found;'
					$scope.resultsFor = $scope.searchParam;
					$scope.searchParam = '';
					$scope.resultadosList = response;
				//}
					$scope.resultados = response.length;
			})	
		}


		$scope.refreshList = function(){
			$scope.postPagoSelected();
			$scope.resultados = 0;
			$scope.transclusion.dateRange = 'last30';
			$scope.resultsFor = '';
		}


 		$scope.filtrarEntreFechasModal = function(url){
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
                controller: 'buscarEntreFechasModalController',
                size: 'md',
                resolve: {
                  url: function(){
					return url;
                  }

                }
            });
            modalInstance.result.then(function (resultadosList) {

				//if(listaPacientes.length > 0){
					//$scope.results = '0 Results Found;'
					$scope.resultsFor = $scope.searchParam;
					$scope.searchParam = '';
					$scope.resultadosList = resultadosList;
					$scope.resultados = resultadosList.length;
				//}
				//$scope.resultados = 0;
            })
 		}

		$scope.queryDate = function(dateRange){

			switch(dateRange) {

			    case 'last30':
			    	var now_date = new Date()
			    	var timestamp_lte = new Date();
			        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
			        break;

			    case 'months-6':
			    	var now_date = new Date()
			    	var timestamp_lte = new Date();
			        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
			        break;

			    default:
			    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
			        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
			} 


			var url = 'api/estudios/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
			$http.get(url).success(function(response ){

					$scope.resultados = response.length;
					$scope.listaPacientes = response;
					function selectOptionText(){
						if($scope.transclusion.dateRange == 'last30'){
							return 'Ultimos 30 dias';
						}else if($scope.transclusion.dateRange == 'months-6'){
							return 'Ultimos 6 meses';
						}else{
							return $scope.transclusion.dateRange;
						}
					}

					$scope.resultsFor = selectOptionText();
					
				
			})	
		
		}


	}])


 	appControllers.controller('codigosController', ['$scope', 'codigos',function( $scope, codigos ){
 		$scope.codigos = codigos;
	}])

 	appControllers.controller('preciosController', ['$scope', 'precios',function( $scope, precios ){
 		$scope.precios = precios;
	}])


 	appControllers.controller('resultadosController', ['$scope', 'resultados', '$uibModal',  '$http', 'pdfServices','$filter',function( $scope, resultados, $uibModal, $http, pdfServices){
 		
 		$scope.resultadosList = resultados;
 		$scope.transclusion = {}
 		$scope.transclusion.dateRange = 'last30';
 		$scope.resultsFor = '';

		$scope.verAdjunto = function(resultado){
			window.open(resultado.adjunto, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
		}

		$scope.verPDF = function(resultado){
			var userData = JSON.parse(sessionStorage.getItem('userDataString'))
			var data = {};
			data.nombres = $filter('capfirstlettereachword')(resultado.paciente.nombres); 
			data.doctor =$filter('capfirstlettereachword')(resultado.medico);
			data.edad = $filter('ageFilter')(new Date(resultado.paciente.fecha_nacimiento));
			data.fecha = $filter('date')(new Date(), 'dd-MMMM-yyyy')
			data.centro_referencia = userData.nomina.laboratorio.razon_social;
			data.material_remitido = 'todo'
			pdfServices.resultadosCitologia(resultado.codigos, data);
		}

 		$scope.mostrarDetallesPaciente = function(paciente){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/detallePacienteModal.html',
	            controller: 'detallePacienteModalController',
	            size: 'md',
	            resolve: {
	              paciente: function(){
	                return paciente;
	              }  
	            }
	        });
 		}

		$scope.detallesResultadoModal = function(resultado){
			if(resultado.tipo =='citologia'){
	            var modalInstance = $uibModal.open({
	                ariaLabelledBy: 'modal-title',
	                ariaDescribedBy: 'modal-body',
	                animation: $scope.animationsEnabled,
	                templateUrl: 'static/templates/modals/detallesResultadosModal.html',
	                controller: 'detallesResultadosModalController',
	                size: 'lg',
	                resolve: {
	                  resultado: function(){
						return resultado;
	                  }
	                }
	            });			
			}

		}


		$scope.refreshList = function(){
			$scope.resultadosList = resultados;
			$scope.resultados = 0;
			$scope.transclusion.dateRange = 'last30';
			$scope.resultsFor = '';
		}


 		$scope.filtrarEntreFechasModal = function(url){
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
                controller: 'buscarEntreFechasModalController',
                size: 'md',
                resolve: {
                  url: function(){
					return url;
                  }

                }
            });
            modalInstance.result.then(function (resultadosList) {

				//if(listaPacientes.length > 0){
					//$scope.results = '0 Results Found;'
					$scope.resultsFor = $scope.searchParam;
					$scope.searchParam = '';
					$scope.resultadosList = resultadosList;
					$scope.resultados = resultadosList.length;
				//}
				//$scope.resultados = 0;
            })
 		}

		// $scope.queryDate = function(dateRange){

		// 	switch(dateRange) {

		// 	    case 'last30':
		// 	    	var now_date = new Date()
		// 	    	var timestamp_lte = new Date();
		// 	        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
		// 	        break;

		// 	    case 'months-6':
		// 	    	var now_date = new Date()
		// 	    	var timestamp_lte = new Date();
		// 	        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
		// 	        break;

		// 	    default:
		// 	    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
		// 	        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
		// 	} 


		// 	var url = 'api/estudios/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
		// 	$http.get(url).success(function(response ){

		// 			$scope.resultados = response.length;
		// 			$scope.listaPacientes = response;
		// 			function selectOptionText(){
		// 				if($scope.transclusion.dateRange == 'last30'){
		// 					return 'Ultimos 30 dias';
		// 				}else if($scope.transclusion.dateRange == 'months-6'){
		// 					return 'Ultimos 6 meses';
		// 				}else{
		// 					return $scope.transclusion.dateRange;
		// 				}
		// 			}

		// 			$scope.resultsFor = selectOptionText();
					
				
		// 	})	
		
		// }
	}])

 	appControllers.controller('pacientesController', ['$scope', 'listaPacientes', '$uibModal', '$http',  'dateService', 'firstPatientDate', '$location',function( $scope, listaPacientes, $uibModal, $http, dateService, firstPatientDate, $location ){
 		
 		$scope.transclusion = {}
 		$scope.transclusion.dateRange = 'last30';
 		$scope.listaPacientes = listaPacientes;
 		$scope.resultsFor = '';


        var end = new Date();
        var begin = new Date(firstPatientDate)

        $scope.yearRange = dateService.yearArray(begin, end);


        $scope.agregar_estudiomodal = function(paciente){

            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
                controller: 'buscarEntreFechasModalController',
                size: 'md',
                resolve: {
                  url: function(){
					return url;
                  }

                }
            });
            modalInstance.result.then(function (listaPacientes) {
				//if(listaPacientes.length > 0){
					//$scope.results = '0 Results Found;'
					$scope.resultsFor = $scope.searchParam;
					$scope.searchParam = '';
					$scope.listaPacientes = listaPacientes;
					$scope.resultados = listaPacientes.length;
				//}
				//$scope.resultados = 0;
            })        	
        }


 		$scope.filtrarEntreFechasModal = function(url){

            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                //animation: $scope.animationsEnabled,
                templateUrl: 'static/templates/modals/buscarEntreFechasModal.html',
                controller: 'buscarEntreFechasModalController',
                size: 'md',
                resolve: {
                  url: function(){
					return url;
                  }

                }
            });
            modalInstance.result.then(function (listaPacientes) {
				//if(listaPacientes.length > 0){
					//$scope.results = '0 Results Found;'
					$scope.resultsFor = $scope.searchParam;
					$scope.searchParam = '';
					$scope.listaPacientes = listaPacientes;
					$scope.resultados = listaPacientes.length;
				//}
				//$scope.resultados = 0;
            })
 		}


 		$scope.tableAction = function(  paciente ){
			switch( paciente.action  ) {

			    case 'Ver Estudios':
			        var modalInstance = $uibModal.open({
			            ariaLabelledBy: 'modal-title',
			            ariaDescribedBy: 'modal-body',
			            animation: $scope.animationsEnabled,
			            templateUrl: 'static/templates/modals/estudiosPacienteModal.html',
			            controller: 'estudiosPacienteModalController',
			            size: 'md',
			            resolve: {
							estudios: function($http){
							    var url = 'api/estudios_realizados/?cedula=' + paciente.cedula +'&impreso=True';
							    return $http({ 
							        method: 'GET', 
							        url: url
							    }).then(function(estudios){
							        return estudios.data;
							    })
							},
							paciente:function(){
									return paciente;
							}
			            }
			        });
			        break;

			    case 'Agregar Estudio':
			    	$location.path('inicio').search({cedula:paciente.cedula, nacionalidad:paciente.nacionalidad})
			        break;

			    case 'Agregar Resultados':
			        var modalInstance = $uibModal.open({
			            ariaLabelledBy: 'modal-title',
			            ariaDescribedBy: 'modal-body',
			            animation: $scope.animationsEnabled,
			            templateUrl: 'static/templates/modals/agregarResultadosModal.html',
			            controller: 'agregarResultadosModalController',
			            size: 'lg',
			            resolve: {
							estudios: function( $http ){
							    var url = 'api/estudios_realizados/?cedula=' + paciente.cedula +'&results_printed=False&impreso=True';
							    return $http({ 
							        method: 'GET', 
							        url: url
							    }).then(function(estudios){
							    	if(estudios.data.results.length ==0){
							    		alert('Paciente no tiene estudios pendientes')
							    		throw true;
							    	}
							        return estudios.data;
							    })
							},
							paciente: function(){
								return paciente
							}
			            }
			        });
			        break;

			    default:
			    	return false;
			} 

 		}



		$scope.queryDate = function(dateRange){

			switch(dateRange) {

			    case 'last30':
			    	var now_date = new Date()
			    	var timestamp_lte = new Date();
			        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
			        break;

			    case 'months-6':
			    	var now_date = new Date()
			    	var timestamp_lte = new Date();
			        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
			        break;

			    default:
			    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
			        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
			} 


			var url = 'api/pacientes/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
			$http.get(url).success(function(response ){

					$scope.resultados = response.length;
					$scope.listaPacientes = response;
					function selectOptionText(){
						if($scope.transclusion.dateRange == 'last30'){
							return 'Ultimos 30 dias';
						}else if($scope.transclusion.dateRange == 'months-6'){
							return 'Ultimos 6 meses';
						}else{
							return $scope.transclusion.dateRange;
						}
					}

					$scope.resultsFor = selectOptionText();
					
				
			})	
		
		}



		$scope.refreshList = function(){
			$scope.listaPacientes = listaPacientes;
			$scope.resultados = 0;
			$scope.transclusion.dateRange = 'last30';
			$scope.resultsFor = '';
		}




		// $scope.searchBackend = function(){
		// 	var url = 'api/pacientes/?search=' + $scope.searchParam;
		// 	console.log($scope.searchParam)
		// 	$http.get(url).success(function(response ){
		// 		console.log(response)
		// 		//if(response.length > 0){
		// 			//$scope.results = '0 Results Found;'
		// 			$scope.resultsFor = $scope.searchParam;
		// 			$scope.searchParam = '';
		// 			$scope.listaPacientes = response;
		// 		//}
		// 			$scope.resultados = response.length;
		// 	})	
		// }


 		$scope.mostrarDetallesPaciente = function(paciente){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/detallePacienteModal.html',
	            controller: 'detallePacienteModalController',
	            size: 'md',
	            resolve: {
	              paciente: function(){
	                return paciente;
	              }  
	            }
	        });
 		}
	}])


 	appControllers.controller('navBarController', ['$scope', '$window', 'userSessionServices', function( $scope, $window, userSessionServices ){
		
 		$scope.navbar_manipulated = false;

 		$scope.salir = function(){
 			userSessionServices.logOut();
 		}

		$scope.toggleCollapse = function(){
			if($window.innerWidth<=768 && $scope.navbar_manipulated == false){
				$scope.navCollapsed = true;
				$scope.$apply()
			}
		}


		if(document.documentElement.clientWidth <=768){
			$scope.navCollapsed = true;
		}

		$scope.navbarToggler = function(){
			if ($scope.navCollapsed == false){			
				$scope.navCollapsed = true;
			}
		}
	}])



	appControllers.controller('homeController', ['$scope', '$uibModal', '$http', 'hotkeys', 'uibDateParser', '$filter', 'estudios', 'arrayServices','pdfServices','agregar_estudio',function( $scope, $uibModal, $http, hotkeys, uibDateParser, $filter, estudios, arrayServices, pdfServices, agregar_estudio ){
		

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


	$scope.clinica_referida_typeahead = estudios.clinicas;
	$scope.medico_referido_typeahead = estudios.medicos;

	$scope.formData = {};
	$scope.estudioData = {};
	$scope.formData.nacionalidad = 'V';
	
	$scope.format = 'ddMMyyyy';
	$scope.estudios = estudios.estudios;
	$scope.selectAll = false;
	$scope.subPruebaTypeahead = [];

	$scope.finanzas = {};
	$scope.finanzas.descuento = 0;
	$scope.displayDiscount = false;

	$scope.form_editable = true;
	$scope.patientFound = false;
	$scope.patch_method = false;

	$scope.pacienteTabList = [
		//{ url : 'auctionproducts', name : 'Register Purchases'  },
		{ url : 'inicio', name : 'Paciente Normal'  },
		{ url : 'paciente_post_pago', name : 'Paciente Post Pago'  }
		//{ url : 'orderhistory', name : 'Order History'  },
		//{ url : 'paymenthistory', name : 'Payment History'  }
		//{ url : 'paymenthistory', name : 'Payment History'  }
	] 

	document.getElementById('cedula').focus();


	$scope.toggleDiscount = function(){
		$scope.displayDiscount = !$scope.displayDiscount;
		if ($scope.displayDiscount == false){
			$scope.finanzas.descuento = 0;
		}
	}

	$scope.fillSubPrueba = function(){
		if( $scope.estudioData.prueba){
			$scope.estudioData.subprueba = '';
			for (var estudio in $scope.estudios){
				if ( $scope.estudios[ estudio ].id  == $scope.estudioData.prueba.id ){
					$scope.subPruebaTypeahead=$scope.estudioData.prueba.sub_tipos_estudios
					//$scope.subPruebaTypeahead= arrayServices.arrayFromObjArray($scope.estudios[ estudio ].sub_tipos_estudios, 'nombre')
					//$scope.subprueba_list = $scope.estudios[ estudio ]['sub_tipos_estudios'];
					break;
					//$scope.subPruebaTypeahead = $scope.estudios[ estudio ].sub_tipos_estudios;
				}else{
					$scope.subprueba_list = [];
				}
				// else if( $scope.estudios[ estudio ].nombre  == 'biopsia' ){
				// 	console.log(arrayServices.arrayFromObjArray($scope.estudios[ estudio ].sub_tipos_estudios, 'nombre'))
				// 	//$scope.subPruebaTypeahead = $scope.estudios[ estudio ].sub_tipos_estudios;
				// }
			}		
		}
	}


	$scope.agregarResultados = function( paciente ){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/modals/agregarResultadosModal.html',
	            controller: 'agregarResultadosModalController',
	            size: 'lg',
	            resolve: {
					estudios: function( $http ){
					    //var url = 'api/estudios_realizados/?cedula=' + paciente.cedula +'&results_printed=False&impreso=True';
					    var url = 'api/estudios_model/?cedula='+ paciente.cedula +'&impreso=True&results_printed=False';
					    return $http({ 
					        method: 'GET', 
					        url: url
					    }).then(function(estudios){
					    	if(estudios.data.length ==0){
					    		alert('Paciente no tiene estudios pendientes')
					    		throw true;
					    	}
					        return estudios.data;
					    })
					},
					paciente: function(){
						return paciente
					}
	            }
	        });

	}

	$scope.selectAllchx = function(){
		//$scope.selectAll = !$scope.selectAll;
		for (var i in $scope.estudiosAgregados){
			//if($scope.estudiosAgregados[i].services.services_present == false){
				$scope.estudiosAgregados[i].checked = $scope.selectAll;
			//}
	
		}
	}

	$scope.modelOptions = {
		debounce: {
		  default: 500,
		  blur: 250
		},
	getterSetter: true
	};

	hotkeys.bindTo($scope)
	.add({
	  combo: 'ctrl+1',
	  description: 'Para agregar examenes a cliente',
	  allowIn: ['INPUT', 'SELECT', 'TEXTAREA'],
	  callback: function() {
	  	$scope.agregarExamen()
	  }
	})
    // you can chain these methods for ease of use:
    //.add ({...});

    $scope.borrarExamenesSelecionados = function(){
    	if ($scope.estudiosAgregados.length>0){

			var del_list = [];
			for (var row in $scope.estudiosAgregados){
				if ($scope.estudiosAgregados[row].checked == true ){
					del_list.push($scope.estudiosAgregados[row].id)
				}
			}
			if (del_list.length == 0){
				alert('No ha seleccionado examenes de la lista');
				return false;
			}


			var delete_answer =  confirm("¿Esta seguro(a) de que desea borrar los estudios seleccionados?");


			if (delete_answer){
				var url = 'api/deleteunprinted/?cedula=' + String($scope.formData.cedula)+ '&impreso=False';
				var data = {}
				data.del_list  = del_list;
				$http.post(url, data).success(function(response, status){
					if(status == 200){
						$scope.estudiosAgregados = response.sub_tipos_estudios;
						alert('Ha borrado los estudios exitosamente');
					}
				})
				.error(function(errors, status){
					console.log(status);
				})
			}else{
				return false;
			}

    	}else{
    		return false;
    	}

    }


    $scope.totalEstudios = function(){
    	var total = 0;
    	if($scope.estudiosAgregados){
			for (var i in $scope.estudiosAgregados){
				total += parseFloat($scope.estudiosAgregados[i].precio)
				
			}
			return total - (total * $scope.finanzas.descuento)/100;
    	}
    	return 0;
    	
    }


    $scope.addEstudio = function(){

    	if ($scope.addPruebaForm.$valid){
    		var url = 'api/estudios/';
    		var data = {};
    		data.paciente = $scope.formData.cedula;
    		data.subprueba = arrayServices.findObjectInArray($scope.subPruebaTypeahead, 'nombre', $scope.estudioData.estudio_realizado).id
    		data.medico = $scope.estudioData.medico;
    		data.clinica = $scope.estudioData.clinica;
    		$http.post(url, data).success(function(response){
				//$scope.clinica_referida_typeahead.push(clinica);
				//$scope.medico_referido_typeahead.push(medico);
    			$scope.estudiosAgregados = response.sub_tipos_estudios;
    			$scope.estudioData = {};
				$scope.addPruebaForm.$setUntouched();
				$scope.addPruebaForm.$setPristine();
    			//$scope.examenesAgregados = response;
    		})
    	}

    }

    $scope.imprimir = function(){
    	if($scope.ingresoPacienteForm.$valid){
	    	var data = {}
	    	data.estudios = arrayServices.arrayFromObjArray($scope.estudiosAgregados, 'id');
	    	data.monto = $scope.totalEstudios();
	    	data.descuento = $scope.finanzas.descuento;
	    	data.rif = $scope.formData.cedula;
	    	data.nombre = $scope.formData.nombres;
	    	data.direccion = $scope.formData.direccion;
	    	data.nacionalidad = $scope.formData.nacionalidad;
	    	data.telefono = $scope.formData.celular;

	    	if($scope.otroCotribuyente == true){
		        var modalInstance = $uibModal.open({
		            ariaLabelledBy: 'modal-title',
		            ariaDescribedBy: 'modal-body',
		            animation: $scope.animationsEnabled,
		            templateUrl: 'static/templates/modals/otroContribuyenteModal.html',
		            controller: 'otroContribuyenteModalController',
		            size: 'md',
		            resolve: {
		              data: function(){
		                return data;
		              }        
		            }
		        });
	    	}else{
	    		var url = 'api/imprimir_estudios/' + String( $scope.formData.cedula )+'/'+ String( $scope.formData.nacionalidad );
		    	$http.post(url, data).success(function(response, status){
		    		if (status == 200){
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

		    			$scope.estudiosAgregados = [];
		    			$scope.finanzas.descuento = 0;
		    			pdfServices.facturaNormal(table_list, client_data );

		    		}else{
		    			alert('Hubo un error al imprimir');
		    		}
		    	})
	    	}
    	}
    }


		$scope.ingresarPaciente= function(){
			if( $scope.ingresoPacienteForm.$valid ){
				var url = 'api/pacientes/';
				if( $scope.patch_method == true ){
					url = url + String( $scope.formData.cedula ) + '/';
					$http.patch( url, $scope.formData ).success( function( response, status ){
						if( status == 200 ){
							//$scope.formData = {};
							//$scope.formData.nacionalidad = 'V';
							$scope.ingresoPacienteForm.$setUntouched();
							$scope.ingresoPacienteForm.$setPristine();
							$scope.patientFound = true;
							$scope.form_editable = false;
							alert( 'Datos de paciente modificados' );
							document.getElementById( 'medico_referido' ).focus();
							$scope.patch_method = false;
							$scope.showCancelarEdicion = false;
						}
					})	
				}else{
					$http.post(url, $scope.formData).success(function( response, status ){
						if( status == 200 ){
							//$scope.formData = {};
							//$scope.formData.nacionalidad = 'V';
							$scope.patientFound = true;
							$scope.patch_method = true;
							$scope.form_editable = false;
							$scope.formData.id  = response.id;
							$scope.ingresoPacienteForm.$setUntouched();
							$scope.ingresoPacienteForm.$setPristine();
							alert('Paciente Registrado');
							document.getElementById('medico_referido').focus();
						}
					})				
				}
				

			}
		}


		$scope.cancelarEdicion= function(){
			//$scope.patientFound = true;
			//$scope.showCancelarEdicion = false;
			$scope.patch_method = false;
			$scope.form_editable  = false;
		}

		$scope.editPatient = function(){
			//$scope.patientFound = false;
			$scope.patch_method = true;
			$scope.form_editable = true;
		}

		$scope.findPatient = function(nacionalidad_in, cedula_in){
			var params = {};
			var url = 'api/verify_patient/';
			if (nacionalidad_in && cedula_in){
				params.cedula = cedula_in;
				params.nacionalidad = nacionalidad_in
			}
			else if( $scope.ingresoPacienteForm.cedula.$valid ){
				$scope.patientFound = false;
				var nacionalidad_temp = $scope.formData.nacionalidad;
				var cedula_temp = $scope.formData.cedula;
				$scope.formData = {
					nacionalidad : nacionalidad_temp,
					cedula : cedula_temp
				};
				var url = 'api/verify_patient/';
				
				params.nacionalidad = $scope.formData.nacionalidad;
				params.cedula = $scope.formData.cedula;
			}
			console.log(url)
			console.log(params)
				$http.post( url, params ).success( function( response, status ){
					if (status == 203){
						$scope.patientFound = false;
						$scope.form_editable = true;
						$scope.patch_method = false;
						$scope.formData.nombres = response.nombres;
						$scope.formData.apellidos = response.apellidos;
						document.getElementById('fecha_nacimiento').focus();
					}else if(status== 204){
						$scope.patientFound = false;
						$scope.form_editable = true;
						$scope.patch_method = false;
						document.getElementById('nombres').focus();
						return false;
					}else if(status== 200){
						response.fecha_nacimiento = uibDateParser.parse(response.fecha_nacimiento, 'yyyy-MM-dd');
						response.cedula  = parseInt(response.cedula);
						$scope.formData = response;
						$scope.patientFound = true;
						$scope.form_editable = false;
						$scope.patch_method = false;
						$scope.estudiosAgregados = response.sub_tipos_estudios;
						document.getElementById('medico_referido').focus();
					}

				})
				//alert('if patient exists find user profile otherwise, leave fields blank')		
		}

	//get the patient if shortcutting from pacientes
	if ( agregar_estudio.nacionalidad && agregar_estudio.cedula){
		$scope.findPatient(agregar_estudio.nacionalidad, agregar_estudio.cedula)
	}

		// $scope.agregarExamen = function(){
	 //        var modalInstance = $uibModal.open({
	 //            ariaLabelledBy: 'modal-title',
	 //            ariaDescribedBy: 'modal-body',
	 //            animation: $scope.animationsEnabled,
	 //            templateUrl: 'static/templates/modals/addTestModal.html',
	 //            controller: 'agregarExamenController',
	 //            size: 'sm'
	 //            // resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
	 //            //   minDate: function(){
	 //            //     return $scope.minDate;
	 //            //   },
	 //            //   maxDate: function(){
	 //            //     return $scope.maxDate;
	 //            //   },
	 //            //    fechaEgreso: function(){
	 //            //     return $scope.fechaEgreso;
	 //            //   }    
	 //            // }
	 //        });
		// }
	
	}])

