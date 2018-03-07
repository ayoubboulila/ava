'use strict';

/* Controllers */

angular.module('PIRC.controllers', []).
  controller('mvtCtl', ['$scope', '$http', function($scope, $http) {
	  $scope.msg="Hello";
	  console.log("aa");
	  $scope.forward = function(){
		  
		  console.log("forward");
		  console.log(URL);
		  
		  $http({
	            method:'POST',
	            url:URL + '/index/forward',
	            headers: {
	               'Content-Type': 'application/json;charset=utf-8'
	            },
	            data:{"speed": $scope.value}
	        })
	        .then(function(resp){
	            console.log(resp);
	        },function(error){
	            console.log(error);
	        });
	  }
	  
$scope.back = function(){
		  
		  console.log("back");
		  
		  $http({
	            method:'POST',
	            url:URL + '/index/backword',
	            headers: {
	               'Content-Type': 'application/json;charset=utf-8'
	            },
	            data:{"speed": $scope.value}
	        })
	        .then(function(resp){
	            console.log(resp);
	        },function(error){
	            console.log(error);
	        });
	  }

$scope.turn_left = function(){
	  
	  console.log("turn_left");
	  
	  $http({
          method:'POST',
          url:URL + '/index/turn_left',
          headers: {
             'Content-Type': 'application/json;charset=utf-8'
          },
          data:{"speed": $scope.value}
      })
      .then(function(resp){
          console.log(resp);
      },function(error){
          console.log(error);
      });
}


$scope.turn_right = function(){
	  
	  console.log("turn_right");
	  
	  $http({
          method:'POST',
          url:URL + '/index/turn_right',
          headers: {
             'Content-Type': 'application/json;charset=utf-8'
          },
          data:{"speed": $scope.value}
      })
      .then(function(resp){
          console.log(resp);
      },function(error){
          console.log(error);
      });
}


$scope.stop = function(){
	  
	  console.log("stop");
	  
	  $http({
          method:'POST',
          url:URL + '/index/stop',
          headers: {
             'Content-Type': 'application/json;charset=utf-8'
          },
          data:{}
      })
      .then(function(resp){
          console.log(resp);
      },function(error){
          console.log(error);
      });
}


$scope.value = 100;
$scope.onSlide = function onSlide (value) {
	console.log('on slide  ' + value +'scope: '+$scope.value);
}

$scope.onSlideEnd = function onSlideEnd(value) {
	console.log('on slide end  ' + value);
}



  }])
  .controller('cameraCtl', ['$scope', '$http', function($scope, $http) {
	  
	  
	  $scope.vid ='https://www.youtube.com/embed/zBIdZ6TMyMk';
	  
	  $scope.servo_up = function(){
		  
		  console.log("servo_up");
		  
		  $http({
	          method:'POST',
	          url:URL + '/index/servo/up',
	          headers: {
	             'Content-Type': 'application/json;charset=utf-8'
	          },
	          data:{}
	      })
	      .then(function(resp){
	          console.log(resp);
	      },function(error){
	          console.log(error);
	      });
	}
	  
	  
 $scope.servo_down = function(){
		  
		  console.log("servo_down");
		  
		  $http({
	          method:'POST',
	          url:URL + '/index/servo/down',
	          headers: {
	             'Content-Type': 'application/json;charset=utf-8'
	          },
	          data:{}
	      })
	      .then(function(resp){
	          console.log(resp);
	      },function(error){
	          console.log(error);
	      });
	}  
	  
	  
 $scope.servo_left = function(){
	  
	  console.log("servo_left");
	  
	  $http({
         method:'POST',
         url:URL + '/index/servo/left',
         headers: {
            'Content-Type': 'application/json;charset=utf-8'
         },
         data:{}
     })
     .then(function(resp){
         console.log(resp);
     },function(error){
         console.log(error);
     });
}	  
	  
	  
 $scope.servo_right = function(){
	  
	  console.log("servo_right");
	  
	  $http({
         method:'POST',
         url:URL + '/index/servo/right',
         headers: {
            'Content-Type': 'application/json;charset=utf-8'
         },
         data:{}
     })
     .then(function(resp){
         console.log(resp);
     },function(error){
         console.log(error);
     });
}	  
	  
	  

 $scope.servo_neutral = function(){
	  
	  console.log("servo_neutral");
	  
	  $http({
        method:'POST',
        url:URL + '/index/servo/init',
        headers: {
           'Content-Type': 'application/json;charset=utf-8'
        },
        data:{}
    })
    .then(function(resp){
        console.log(resp);
    },function(error){
        console.log(error);
    });
}	  
 
 
	  

  }])
  . controller('speechCtrl', ['$scope', '$http', function($scope, $http) {
	  
	  $scope.speech="";
	  
	  $scope.speak = function(){
		  
		  console.log("speak");
		  console.log($scope.speech);
		  
		  $http({
	        method:'POST',
	        url:URL + '/tts/speak',
	        headers: {
	           'Content-Type': 'application/json;charset=utf-8'
	        },
	        data:{"sentence": $scope.speech}
	    })
	    .then(function(resp){
	        console.log(resp);
	    },function(error){
	        console.log(error);
	    });
	}	
	  
  }]);
