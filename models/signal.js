// Dependencies
var restful = require('node-restful');
var mongoose = restful.mongoose;

// Schema
var signal = new mongoose.Schema({
	user	  : String,
	date	  : String,
	channel	  : String,
	expiration: Number,
	signal: {
		par   : String,
		time  : String,
		action: String,
		status: String
	}	
});

module.exports = restful.model('signal', signal);