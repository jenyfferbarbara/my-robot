angular.module('angularApp', [])

.controller('indexController', function ($scope, $filter, $http) {
  
	// Initialize variables
	$scope.timeframes = [
		{ name: '01', id: '1' },
		{ name: '05', id: '5' },
		{ name: '15', id: '15'}];

	get_users_settings();
	get_channels();

	$scope.selectedUsers = function() {
		$scope.application.users = $filter('filter')($scope.users, {
			checked: true
		});		
	}

	$scope.reset = function () {
		get_users_settings();
	}
	
	$scope.postdata = function() {
		var today = $filter('date')(new Date(), "yyyy-MM-dd");
		var now   = $filter('date')(new Date(), "HH:mm");

		$scope.channels.forEach(channel => {
			if($scope.application.users && channel.list){
				$scope.application.users.forEach(user => {
					var date    = $filter('date')(channel.date, "yyyy-MM-dd");
					var entries = channel.list.split("\n");
					entries.forEach(entry => {
						entry = entry.split(";")
						var data = {
							"user"		: user.name,
							"date"		: date,
							"channel"	: channel.name,
							"expiration": channel.timeframe,
							"signal": {
								"par" 		: entry[0],
								"time"		: entry[1],
								"action"    : entry[2].trim(),
								"status"    : today < date || (today == date && now < entry[1]) ? 'Pending' : 'Delayed'
							}			
						}
						$http.post('/api/signals' , JSON.stringify(data)).then(function (response) {
							if (response.data)
								$scope.msg = "Post Signals Data Submitted Successfully!";
							}, function (response) {
								$scope.msg = "Service not Exists";
								$scope.statusval = response.status;
								$scope.statustext = response.statusText;
								$scope.headers = response.headers();
						});
					});

					value     = user.value
					payout    = 0.87
					recovery  = 0
					profit 	  = value * payout
					stop_loss = 0
					for(var i = 0; i < channel.stop_loss * 2; i++){
						recovery = (profit + recovery) / payout
						stop_loss = stop_loss + recovery
					}

					var data = {
						"user"		: user.name,
						"date"		: date,
						"channel"	: channel.name,
						"expiration": channel.timeframe,
						"stop_win"  : (channel.stop_win * profit).toFixed(),
						"stop_loss" : stop_loss.toFixed(),
						"profit"	: 0,
						"recovery"	: 0,
						"win"		: 0,
						"loss"		: 0
					}

					$http.post('/api/summaries', JSON.stringify(data)).then(function (response) {
						if (response.data)
							$scope.msg = "Post Summaries Data Submitted Successfully!";
						}, function (response) {
							$scope.msg = "Service not Exists";
							$scope.statusval = response.status;
							$scope.statustext = response.statusText;
							$scope.headers = response.headers();
					});
				});				
			}
		});
	}

	function get_users_settings() {
		url = '/api/settings'
		$http.get(url).then(function (response) {
			$scope.users = response.data;
		});
	}

	function get_channels() {		
		url = '/api/channels'
		$http.get(url).then(function (response) {
			$scope.channels = $filter('filter')(response.data, {
				active: true
			});
		});
	}
	
	$scope.application = {
		users: []
	  }

	$scope.postdata_old = function () {
		$http.get('/run_robot?user=' + this.account + '&wallet=' + this.wallet 
		+ '&stop_win=' + this.stop_win + '&stop_loss=' + this.stop_loss + '&expiration=' + this.expiration 
		+ '&channel=' + this.channel).then(function (response) {
			if (response.data)
					$scope.msg = "Run robot Successfully!";
				}, function (response) {
					$scope.msg = "Service not Exists";
					$scope.statusval = response.status;
					$scope.statustext = response.statusText;
					$scope.headers = response.headers();
		});
	};
})