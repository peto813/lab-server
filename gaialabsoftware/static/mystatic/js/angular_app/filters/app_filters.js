
gaiaApp = angular.module('gaiaAppFilters',[]);

gaiaApp.filter('ageFilter', function() {


     function calculateAge(birthday) { // birthday is a date
         var ageDifMs = Date.now() - birthday.getTime();
         var ageDate = new Date(ageDifMs); // miliseconds from epoch
         return Math.abs(ageDate.getUTCFullYear() - 1970);
     }

     // function monthDiff(d1, d2) {
     //   if (d1 < d2){
     //    var months = d2.getMonth() - d1.getMonth();
     //    return months <= 0 ? 0 : months;
     //   }
     //   return 0;
     // }

      function dateDiffInDays(a, b) {
        var _MS_PER_DAY = 1000 * 60 * 60 * 24;
        // Discard the time and time-zone information.
        var utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
        var utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

        return Math.floor((utc2 - utc1) / _MS_PER_DAY);
      }


      function monthDiff(d1, d2) {
          var months;
          months = (d2.getFullYear() - d1.getFullYear()) * 12;
          months -= d1.getMonth() + 1;
          months += d2.getMonth();
          return months <= 0 ? 0 : months;
      }

     return function(birthdate) { 
           var age = calculateAge(birthdate);
           if (age == 0){
              var dayDiff = dateDiffInDays(birthdate, new Date()) 
              if(dayDiff < 31){
                return String(dayDiff) + ' dias'
              }
            return monthDiff(birthdate, new Date()) + ' Meses';
           }
              // if( monthDiff(birthdate, new Date()) < 31  ){
              //   return dateDiffInDays(birthdate, new Date()) +' dias';
              // }
             //return monthDiff(birthdate, new Date()) + ' Meses';
           return age;
     }; 
});



gaiaApp.filter('sexoFilter', function() {
     return function(sexo_inicial) { 
      if(sexo_inicial=='M'){
        return 'Masculino';
      }else if(sexo_inicial=='F'){
        return 'Femenino';
      }else{
        return 'indefinido';
      }
     }; 
     // function calculateAge(birthday) { // birthday is a date
     //     var ageDifMs = Date.now() - birthday.getTime();
     //     var ageDate = new Date(ageDifMs); // miliseconds from epoch
     //     return Math.abs(ageDate.getUTCFullYear() - 1970);
     // }
     // function monthDiff(d1, d2) {
     //   if (d1 < d2){
     //    var months = d2.getMonth() - d1.getMonth();
     //    return months <= 0 ? 0 : months;
     //   }
     //   return 0;
     // }       
     // return function(birthdate) { 
     //       var age = calculateAge(birthdate);
     //       if (age == 0)
     //         return monthDiff(birthdate, new Date()) + ' Meses';
     //       return age;
     // }; 
});

gaiaApp.filter('capitalize', function() {
    return function(input) {
      return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
});


gaiaApp.filter('capfirstlettereachword', function() {
    return function(input) {
      if (input){
            var splitStr = input.toLowerCase().split(' ');
            for (var i = 0; i < splitStr.length; i++) {
                splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
            }
            return splitStr.join(' ');      
      }

    };
})

gaiaApp.filter('toJsonObj', function() {
    return function(input) {
        return JSON.parse(input);
      // if (input){
      //       var splitStr = input.toLowerCase().split(' ');
      //       for (var i = 0; i < splitStr.length; i++) {
      //           splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
      //       }
      //       return splitStr.join(' ');      
      // }

    };
})

gaiaApp.filter('unique', function() {
      return function uniq_fast(a) {
      var seen = {};
      var out = [];
      var len = a.length;
      var j = 0;
      for(var i = 0; i < len; i++) {
           var item = a[i];
           if(seen[item] !== 1) {
                 seen[item] = 1;
                 out[j++] = item;
           }
      }
      return out;
  }
});