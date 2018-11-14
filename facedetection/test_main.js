(function () {
    var gn;

    window.addEventListener('DOMContentLoaded', function () {
        var isStreaming = false;
        //var video = document.getElementById('v');
        // var left = document.getElementById('left');
        // var right = document.getElementById('right');
        // var forward = document.getElementById('forward');
        // var backward = document.getElementById('backward');
        // var start = document.getElementById('start');
        // var stop = document.getElementById('stop');
        var address = "10.0.0.22/webrtc"
        var protocol = location.protocol === "https:" ? "wss:" : "ws:";
        var wsurl = protocol + '//' + address;

        if (!isStreaming) {
            signal(wsurl,
                    function (stream) {
                        console.log('got a stream!');
                        var url = window.URL || window.webkitURL;
                        //video.src = url ? url.createObjectURL(stream) : stream;
                       // video.src = "http://10.0.0.22:8080/stream/video.mjpeg"
                        //video.play();
                    },
                    function (error) {
                        alert(error);
                    },
                    function () {
                        console.log('websocket closed. bye bye!');
                        //video.src = '';
                    },
                    function (message) {
                        console.log(message);
                        //alert(message);
                    }
            );
        }

        // left.addEventListener('click', function (e) {
        //     send_message(5);
        // }, false);

        // right.addEventListener('click', function (e) {
        //     send_message(6);
        // }, false);
        // forward.addEventListener('click', function (e) {
        //     send_message(7);
        // }, false);

        // backward.addEventListener('click', function (e) {
        //     send_message(8);
        // }, false);

        // start.addEventListener('click', function (e) {
        //     send_message(9);
        // }, false);

        // stop.addEventListener('click', function (e) {
        //     send_message(0);
        // }, false);

        window.addEventListener('keydown', function (e){
           //console.log(e.which); 
           switch (e.which){
                case 37: //left
                    console.log("left")
                    send_message(5);
                    break;
                case 39: //right
                    console.log("right")
                    send_message(6);
                    break;
                case 38: //up
                    console.log("forward");
                    send_message(7);
                    break;
                case 40: //down
                    console.log("backward");
                    send_message(8);
                    break;
                case 79: //on - o
                    console.log("on");
                    send_message(9);
                    break;
                case 80: //up - p
                    console.log("off");
                    send_message(0);
                    break;
           }
        }, false);

        window.addEventListener('keyup', function (e){
           //console.log("keyup");
           //console.log(e.which); 
           switch (e.which){
                case 37: //left
                case 39: //right
                case 38: //up
                case 40: //stop
                    console.log("pause");
                    send_message(0);
                    break;
           }
        }, false);

       // addGyronormScript();
       startGyro();
       //console.log(gn);

    });

    function handleOrientation(event) {
        var data = {
            "do": {
                "alpha": event.alpha.toFixed(1), // In degree in the range [0,360]
                "beta": event.beta.toFixed(1), // In degree in the range [-180,180]
                "gamma": event.gamma.toFixed(1), // In degree in the range [-90,90]
                "absolute": event.absolute
            }
        };
        if (datachannel)
            datachannel.send(JSON.stringify(data));
    }

    function handleGyronorm(data) {
        // Process:
        // data.do.alpha    ( deviceorientation event alpha value )
        // data.do.beta     ( deviceorientation event beta value )
        // data.do.gamma    ( deviceorientation event gamma value )
        // data.do.absolute ( deviceorientation event absolute value )

        // data.dm.x        ( devicemotion event acceleration x value )
        // data.dm.y        ( devicemotion event acceleration y value )
        // data.dm.z        ( devicemotion event acceleration z value )

        // data.dm.gx       ( devicemotion event accelerationIncludingGravity x value )
        // data.dm.gy       ( devicemotion event accelerationIncludingGravity y value )
        // data.dm.gz       ( devicemotion event accelerationIncludingGravity z value )

        // data.dm.alpha    ( devicemotion event rotationRate alpha value )
        // data.dm.beta     ( devicemotion event rotationRate beta value )
        // data.dm.gamma    ( devicemotion event rotationRate gamma value )
        if (datachannel)
            //datachannel.send(data);
            datachannel.send(JSON.stringify(data));
    }

    function startGyro(){
        console.log("gyronorm.js library found!");
        if (gn) {
            gn.setHeadDirection();
            return;
        }
        try {
            gn = new GyroNorm();
        } catch (e) {
            console.log(e);
            return;
        }
        var args = {
            frequency: 60, // ( How often the object sends the values - milliseconds )
            gravityNormalized: true, // ( If the gravity related values to be normalized )
            orientationBase: GyroNorm.GAME, // ( Can be GyroNorm.GAME or GyroNorm.WORLD. gn.GAME returns orientation values with respect to the head direction of the device. gn.WORLD returns the orientation values with respect to the actual north direction of the world. )
            decimalCount: 1, // ( How many digits after the decimal point will there be in the return values )
            logger: null, // ( Function to be called to log messages from gyronorm.js )
            screenAdjusted: false            // ( If set to true it will return screen adjusted values. )
        };
        gn.init(args).then(function () {
            gn.start(handleGyronorm);
            gn.setHeadDirection(); // only with gn.GAME
        }).catch(function (e) {
            console.log("DeviceOrientation or DeviceMotion might not be supported by this browser or device");
        });
        
        if (!gn) {
            window.addEventListener('deviceorientation', handleOrientation, true);
            console.log("gyronorm.js library not found, using defaults");
        }
    }
})();