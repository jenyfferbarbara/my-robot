angular.module('angularApp', [])

.controller('postserviceCtrl', function ($scope, $filter, $http) {
  
	// Initialize variables
	this.account    = null;
	this.wallet     = null;
	this.expiration = null;
	this.stop_win   = null;
	this.stop_loss  = null;
	this.channel    = null;
	this.list       = null;

	$scope.reset = function () {
		this.account    = null;
		this.wallet     = null;
		this.expiration = null;
		this.stop_win   = null;
		this.stop_loss  = null;
		this.channel    = null;
		this.list       = null;
	}

	$scope.postdata = function () {
		var date = $filter('date')(new Date(), "yyyy-MM-dd");
		var now = $filter('date')(new Date(), "HH:mm");
		var entries = this.list.split("\n")

		entries.forEach(entry => {
			entry = entry.split(";")

			var data = {
				"_id": {
					"user": this.account,
					"par" : entry[0],
					"date": date,
					"time": entry[1]
				},
				"action"    : entry[2].trim(),
				"expiration": this.expiration,
				"profit"    : 0,
				"status"    : now <= entry[1] ? 'Pending' : 'Delayed'
			}
			
			$http.post('http://vps31866.publiccloud.com.br:8080/api/' + this.channel, JSON.stringify(data)).then(function (response) {
				if (response.data)
					$scope.msg = "Post Data Submitted Successfully!";
				}, function (response) {
					$scope.msg = "Service not Exists";
					$scope.statusval = response.status;
					$scope.statustext = response.statusText;
					$scope.headers = response.headers();
			});
		});

		$http.get('http://vps31866.publiccloud.com.br:8080/run_robot?user=' + this.account + '&wallet=' + this.wallet 
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