angular.module('angularApp', [])

.controller('configController', function ($scope, $filter, $http) {
  
	$scope.wallets = [
		{ name: 'Demo', id: 'PRACTICE' },
		{ name: 'Real', id: 'REAL'}];

	get_users_settings();

	function get_users_settings() {		
		url = '/api/settings'
		$http.get(url).then(function (response) {
			$scope.users_settings = response.data;
		});
	}
	
	$scope.reset = function () {
		get_users_settings();
	}

	$scope.postdata = function () {
		$scope.users_settings.forEach(user => {
			var data = {
				"name"     : user.name,
				"email"    : user.email,
				"password" : user.password,
				"wallet"   : user.wallet,
				"value"    : user.value,
				"stop_win" : user.stop_win,
				"stop_loss": user.stop_loss
			}
			
			$http.put('/api/settings/' + user._id, JSON.stringify(data)).then(function (response) {
				if (response.data)
					$scope.msg = "Post Data Submitted Successfully!";
				}, function (response) {
					$scope.msg = "Service not Exists";
					$scope.statusval = response.status;
					$scope.statustext = response.statusText;
					$scope.headers = response.headers();
			});
		});
	};
})