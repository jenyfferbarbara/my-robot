// Dependencies
var express = require('express');
var router  = express.Router();

// Models
var Users               = require('../models/settings');
var Fox                 = require('../models/fox');
var Rafa_CR7            = require('../models/rafa_cr7');
var Sinais_Consistentes = require('../models/sinais_consistentes');
var SlumSignals         = require('../models/slum_signals');
var Testes              = require('../models/testes');

// Routes
Users.methods(['get', 'put', 'post', 'delete']);
Users.register(router, '/settings');

Fox.methods(['get', 'put', 'post', 'delete']);
Fox.register(router, '/fox');

Rafa_CR7.methods(['get', 'put', 'post', 'delete']);
Rafa_CR7.register(router, '/rafa_cr7');

Sinais_Consistentes.methods(['get', 'put', 'post', 'delete']);
Sinais_Consistentes.register(router, '/sinais_consistentes');

SlumSignals.methods(['get', 'put', 'post', 'delete']);
SlumSignals.register(router, '/slum_signals');

Testes.methods(['get', 'put', 'post', 'delete']);
Testes.register(router, '/testes');

// Return router
module.exports = router;