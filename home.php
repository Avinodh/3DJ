<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <meta charset=utf-8>
        <link rel="stylesheet" href="style.css" type="text/css">
        
        <title>DJ 3D</title>
        <link href='http://fonts.googleapis.com/css?family=Raleway:300' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=PT+Mono' rel='stylesheet' type='text/css'>
        
        <script>                                                                                     
        var volume = 12;                //Initialising equilibrium volume                                                                 
        var myGain;                                                                                  
        </script>

        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
        <script type="text/javascript" src='remix.js'></script>
        <script type="text/javascript" src='fetch.js'></script> 

        <script type="text/javascript">             //Script for Loading an controlling music
            // First-beat extraction and assembly
            // You will need to supply your Echo Nest API key, the trackID, and a URL to the track.
            // The supplied track in this case is 1451_-_D.mp3.
            var apiKey = 'YOUR_ECHO_NEST_KEY';
            var trackID = 'TRACK_ID';
            var trackURL = '1451_-_D.mp3';
            var DJURL = 'DJ.mp3'; 
            var remixer;
            var player;
            var track;
            var remixed;
            var Context;

            function init() {
                var contextFunction = window.webkitAudioContext || window.AudioContext;
                if (contextFunction === undefined) {
                    $("#info").text("Sorry, this app needs advanced web audio. Your browser doesn't"
                        + " support it. Try the latest version of Chrome?");
                } else {
                    var context = new contextFunction();
                    Context = context;
                    remixer = createJRemixer(context, $, apiKey);
                    player = remixer.getPlayer();

                    $("#info").text("Loading analysis data...");
                    remixer.remixTrackById(trackID, trackURL, function(t, percent) {
                        track = t;
                        $("#info").text(percent + "% of the track loaded");
                        if (percent == 100) {
                            $("#info").text(percent + "% of the track loaded, touching up...");
                        }
                        if (track.status == 'ok') {
                            remixed = new Array();
                            // Do the remixing here!
                            for (var i=0; i < track.analysis.beats.length; i++) {
                                if (i % 4 == 0) {
                                    remixed.push(track.analysis.beats[i])
                                }
                            }
                            $("#info").text("Track Ready!");
                        }
                    });
                }
            }
            window.onload = init;
            $(window).keydown(function(e) {
                if (e.keyCode == 32) {
                    console.log('Space pressed');
                    player.queue(track.analysis.beats[1]);
                }

                if(e.keyCode == 65){
                    player.queue(track.analysis.bars[1]);
                }

                if(e.keyCode == 66 || volume < 12)
                {
                    myGain.gain.value*= 0.5;
                    aud = 0;
                }

                if(e.keyCode == 69)
                {
                    var snd = new Audio(DJURL);
                    snd.play();
                }

                if(e.keyCode == 67 || volume > 12)
                {
                    myGain.gain.value*= 2;
                }

                if(e.keyCode == 68)
                {
                    console.log('d is pressed');
                    // Create the filter
                    var filter = Context.createBiquadFilter();
                    // Create the audio graph.
                    mySource.connect(filter);
                    filter.connect(Context.destination);
                    // Create and specify parameters for the low-pass filter.
                    filter.type = 'lowpass'; // Low-pass filter. See BiquadFilterNode docs
                    filter.frequency.value = 440; // Set cutoff to 440 HZ
                    // Playback the sound.
                    //mySource.stop();
                    //ySource.start(0);
                }
            });

        </script>

    </head>

    <body>
        <div class = "everything">
            <div id ="header" style="width:100%;height:80px;padding-top:0px;padding-bottom:3px;background-color:#2574A9;">
                <img style="height:70px;margin-left:25px;margin-right:10px;box-shadow:1px 2px 5px black;border:1px solid white;border-radius:50%;background-color:transparent;" src="https://lh4.ggpht.com/NjSeU8ya6h8cNL6JntWZqhlkmAHKcy0vJmxDBqF0x_y4izs6skpxg6a4TRsf3Jza7kk=w300"/>
                <h2> 3DJ. Shape Your Music </h2>
            </div>

            <div class ="wrapper">
                <div id = "text" style="margin-top:50px;">
                    <h2 style="color:red;font-size:12px;font-weight:bold;">(Host currently inactive. Myo and LEAP sensors not detected. Music will default to 0 Volume.)</h2>
                     <span style="color:gray;">Welcome to 3DJ!!!</span>
                    <div id='info'> </div>
                    <button onClick="player.play(0, remixed);" type ="button" class="btn btn-success btn-lg">Play!</button>
                    <button  onClick="player.stop()" type="button" class="btn btn-danger btn-lg" >Stop!</button>
                </div>
            </div>

            <div style="padding-top:10px;overflow-y:scroll;background-color:black;color:white;width:100%;height:200px;overflow-y:scroll;font-size:10px;" id="response">
                <span style="text-decoration:underline;">Myo Feedback Vertical Axis (1-18 scale):</span><br>
            </div>
            
            <div id ="About" style="width:100%;text-align:center;">
                <h3>About</h3>
                The hack made by 4 ambitious students from UCLA gives a completley new way to play around with a song playing available on Spotify. Using Myo and Leap sensors, we detect various motions and process them in order to provide an output which is a remixed version of the track playing in real time. The possibilities are endless. You can take DJing to a whole new level. But that's not all. The display is hooked to an Oculus Rift through which you can see an equalizer which gets updated dynamically depending on what you do with the music. Get immersed in a virtual reality environment and experience music in a completley new way with more control than ever. DJ 3D. How will you shape your music? 
            </div>
        </div>
    </body>
</html>
