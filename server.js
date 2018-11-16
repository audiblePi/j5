var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var SerialPort = require('serialport');
const { exec } = require('child_process');

var port;
findSerialPort();
//app.use(express.static('public'));

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
    // exec('gpio pwm-ms');
    // exec('gpio pwmc 192');
    // exec('gpio pwmr 2000');
    //console.log('a user connected');
});

// app.get('/cv.html', function(req, res){
//     res.sendFile(__dirname + '/cv.html');
// });

// app.get('/cv.js', function(req, res){
//     res.sendFile(__dirname + '/cv.js');
// });

// app.get('/cv.data', function(req, res){
//     res.sendFile(__dirname + '/cv.data');
// });

// app.get('/face-detection.js', function(req, res){
//     res.sendFile(__dirname + '/face-detection.js');
// });

// app.get('/main.js', function(req, res){
//     res.sendFile(__dirname + '/main.js');
// });

// app.get('/signalling.js', function(req, res){
//     res.sendFile(__dirname + '/signalling.js');
// });

app.get('/control', function(req, res){
    res.sendFile(__dirname + '/control.html');
    exec('gpio pwm-ms');
    exec('gpio pwmc 192');
    exec('gpio pwmr 2000');
});

app.get('/move/:cmd', function (req, res) {
    res.send(req.params.cmd)
    command(req.params.cmd)
})

io.on('connection', function(socket){
    console.log('a user connected');

    socket.on('disconnect', function(){
        console.log('user disconnected');
    });

    socket.on('chat message', function(msg){
        io.emit('chat message', msg);    
        console.log('chat: ' + msg);
    });

    socket.on('move', function(msg){
        moveCommand(msg);
        console.log('move: ' + msg);
    });

    socket.on('pan', function(msg){
        pan(msg);
        console.log('pan: ' + msg);
    });

    socket.on('tilt', function(msg){
        tilt(msg);
        console.log('tilt: ' + msg);
    });

    socket.on('do-alpha', function(msg){
        //handleDO(msg);
        //console.log('do-alpha: ' + msg);
        pan(msg)
    });

    socket.on('do-beta', function(msg){
        //handleDO(msg);
        //console.log('do-beta: ' + msg);
    });

    socket.on('do-gamma', function(msg){
        //handleDO(msg);
        //console.log('do-gamma: ' + msg);
        tilt(msg)
    });

    // socket.on('reset', function(msg){
    //     var command1 = 'gpio -g pwm 13 180'
    //     var command2 = 'gpio -g pwm 18 150'
    //     exec(command1, execCallback);
    //     exec(command2, execCallback);
    // });
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});

function moveCommand(int){
    port.write(int, function(err) {
        if (err) {
            return console.log('Error on write: ', err.message);
        }
    });
}

function pan(int){
    var command = 'gpio -g pwm 18 ' + int
    exec(command, execCallback);
}

function tilt(int){
    var command = 'gpio -g pwm 13 ' + int
    exec(command, execCallback);
}

function execCallback (error, stdout, stderr) {
    if (error) {
        console.error(`exec error: ${error}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
}

function findSerialPort(){
    var serial = '/dev/ttyACM0';
    
    exec('ls /dev/ttyACM*', (error, stdout, stderr) => {
        console.log(`stdout: ${stdout}`);
        console.log(`stderr: ${stderr}`);

        if (error) {
            console.error(`exec error: ${error}`);
            return false;
        }
        else{
            var ttyACM = stdout.trim();
            port = new SerialPort(ttyACM, {
                baudRate: 9600
            });
            console.log(`Serial device conected on ${ttyACM}`);
            return true
        }
    });
}