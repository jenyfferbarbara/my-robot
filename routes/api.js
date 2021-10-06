// Dependencies
var express = require('express');
var router  = express.Router();

// Models
var Users     = require('../models/settings');
var Channels  = require('../models/channel');
var Signals   = require('../models/signal');
var Summaries = require('../models/summary');

// Routes
Users.methods(['get', 'put', 'post', 'delete']);
Users.register(router, '/settings');

Channels.methods(['get', 'put', 'post', 'delete']);
Channels.register(router, '/channels');

Signals.methods(['get', 'put', 'post', 'delete']);
Signals.register(router, '/signals');

Summaries.methods(['get', 'put', 'post', 'delete']);
Summaries.register(router, '/summaries');

// Return router
module.exports = router;