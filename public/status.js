angular.module('statusApp', [])

.controller('statusController', function ($scope, $filter, $http) {
  
	get_users_settings();
	$scope.channels = {}

	function get_users_settings() {
		url = '/api/settings'
		$http.get(url).then(function (response) {
			$scope.users = response.data;
		});
	}

	function get_summaries() {
		var date = $filter('date')($scope.date, "yyyy-MM-dd");
		var user = $scope.user;
		
		url = '/api/summaries?user=' + user + '&date=' + date
		$http.get(url).then(function (response) {
			
			response.data.forEach(summary => {
				get_signals(summary);
			});

			$scope.summaries = response.data;
		});
	}

	function get_signals(summary) {
		var date 		= summary.date;
		var user 		= summary.user;
		var channel 	= summary.channel;
		var expiration  = summary.expiration;
		
		url = '/api/signals?user=' + user + '&date=' + date + '&channel=' + channel + '&expiration=' + expiration
		$http.get(url).then(function (response) {
			$scope.channels[summary.channel] = response.data;
		});
	}

	$scope.update_results = function () {	
		get_summaries();
	};

	$scope.cancel = function (sig) {

		var data = {
			"signal": {
				"par" 		: sig.signal.par,
				"time"		: sig.signal.time,
				"action"    : sig.signal.action,
				"status"    : 'Canceled'
			}	
		}

		$http.put('/api/signals/' + sig._id, JSON.stringify(data)).then(function (response) {
			if (response.data)
				$scope.msg = "Post Data Submitted Successfully!";
				get_summaries();
			}, function (response) {
				$scope.msg = "Service not Exists";
				$scope.statusval = response.status;
				$scope.statustext = response.statusText;
				$scope.headers = response.headers();
		});
	}
})