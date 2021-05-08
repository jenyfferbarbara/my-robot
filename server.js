// Dependencies
const express = require('express');
const mongoose = require('mongoose');
const {spawn} = require('child_process');

// mongoDB
const mongoURL = 'mongodb://myRobot:6eJ%402chTyxn2%2as@localhost:27017/my_robot?authSource=admin';
mongoose.connect(mongoURL, {useNewUrlParser: true, useUnifiedTopology: true});

// Express
const app = express();
app.use(express.static('public')); // Server static files
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Routes
app.use('/api', require('./routes/api'));

app.get('/install', (req, res) => {

	var dataToSend;
	const python = spawn('python', ['./api/setup.py', 'install']);

	python.stdout.on('data', function (data) {
		dataToSend = data.toString();
	});

	python.on('close', (code) => {
		res.send(dataToSend)
	});	
})

app.get('/run_robot', (req, res) => {
	const user       = req.query.user
	const wallet     = req.query.wallet
	const stop_win   = req.query.stop_win
	const stop_loss  = req.query.stop_loss
	const expiration = req.query.expiration
	const channel    = req.query.channel

	var dataToSend;
	const python = spawn('python', ['./iq_option/main.py', user, wallet, stop_win, stop_loss, expiration, channel]);

	python.stdout.on('data', function (data) {
		dataToSend = data.toString();
	});

	python.on('close', (code) => {
		res.send(dataToSend)
	});	
})

// Start server
const port = 8080;
app.listen(port);
console.log(`Server is running on port: ${port}`);