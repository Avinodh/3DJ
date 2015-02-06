$(document).ready(function(){
  var flag=1;
  function fetch(){
    if(flag==1){
        $.post("cleardb.php",function(data){console.log(data);}); 
    }

    $.get("control.php",{access:flag},function(data,status){
        if(data=="no-data"){
  	      flag=1;
          setTimeout(fetch, 100);
        }
        else{
          volume = data; 
          
          $("#response").append("&nbsp<p style='line-height:0.5px;display:inline-block;'>"+volume+" </p>");
          if(volume < 12){
              myGain.gain.value*= 0.5;
  	      }
          
          else{
             myGain.gain.value*= 2;
          }
      
          flag++;
          setTimeout(fetch, 100);
        }
    });
  }
  fetch(); 
}); 
