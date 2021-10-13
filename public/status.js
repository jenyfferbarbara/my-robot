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
			console.log("signals: " + response.data);
			$scope.channels[summary.channel] = response.data;
		});
	}

	$scope.update_results = function () {	
		get_summaries()
	};

	// Initialize variables
	this.account = null;

	$scope.getdata = function () {
		var user = this.account;
		var date = $filter('date')(new Date(), "yyyy-MM-dd");

		//Call the services  
		get_results_bear(user, date);
		get_results_rafa_cr7(user, date);
		get_results_sinais_consistentes(user, date);
		get_results_slum_signals(user, date)
	};

	function get_results_bear(user, date) {
		
		url = '/api/fox?_id.user=' + user + '&_id.date=' + date
		$http.get(url).then(function (response) {

			// M5
			var list_M5 = response.data.filter(function(val) {
				return val["expiration"] == 5; }, 0)

			$scope.fox_M5_profit = list_M5.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.fox_M5_win = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.fox_M5_loss = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.fox_M5 =  list_M5
		});
	}

	function get_results_rafa_cr7(user, date) {

		url = '/api/rafa_cr7?_id.user=' + user + '&_id.date=' + date
		$http.get(url).then(function (response) {

			// M5
			var list_M5 = response.data.filter(function(val) {
				return val["expiration"] == 5; }, 0)

			$scope.rafa_cr7_M5_profit = list_M5.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.rafa_cr7_M5_win = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.rafa_cr7_M5_loss = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.rafa_cr7_M5 =  list_M5

			// M15
			var list_M15 = response.data.filter(function(val) {
				return val["expiration"] == 15; }, 0)

			$scope.rafa_cr7_M15_profit = list_M15.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.rafa_cr7_M15_win = list_M15.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.rafa_cr7_M15_loss = list_M15.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.rafa_cr7_M15 =  list_M15
		});
	}

	function get_results_sinais_consistentes(user, date) {

		url = '/api/sinais_consistentes?_id.user=' + user + '&_id.date=' + date
		$http.get(url).then(function (response) {

			// M1
			var list_M1 = response.data.filter(function(val) {
				return val["expiration"] == 1; }, 0)

			$scope.sinais_consistentes_M1_profit = list_M1.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.sinais_consistentes_M1_win = list_M1.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.sinais_consistentes_M1_loss = list_M1.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.sinais_consistentes_M1 =  list_M1

			// M5
			var list_M5 = response.data.filter(function(val) {
				return val["expiration"] == 5; }, 0)

			$scope.sinais_consistentes_M5_profit = list_M5.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.sinais_consistentes_M5_win = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.sinais_consistentes_M5_loss = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.sinais_consistentes_M5 =  list_M5
		});
	}

	function get_results_slum_signals(user, date) {

		url = '/api/slum_signals?_id.user=' + user + '&_id.date=' + date
		$http.get(url).then(function (response) {

			// M1
			var list_M1 = response.data.filter(function(val) {
				return val["expiration"] == 1; }, 0)

			$scope.slum_signals_M1_profit = list_M1.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.slum_signals_M1_win = list_M1.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.slum_signals_M1_loss = list_M1.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.slum_signals_M1 =  list_M1

			// M5
			var list_M5 = response.data.filter(function(val) {
				return val["expiration"] == 5; }, 0)

			$scope.slum_signals_M5_profit = list_M5.reduce(function(acc, val) { 
				return acc + val["profit"]; }, 0).toFixed(2)
			
			$scope.slum_signals_M5_win = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "WIN" ? 1 : 0;
				return acc + value; }, 0)

			$scope.slum_signals_M5_loss = list_M5.reduce(function(acc, val) {
				var value = val["result"] == "LOSS" ? 1 : 0;
				return acc + value; }, 0)

			$scope.slum_signals_M5 =  list_M5
		});
	}
})