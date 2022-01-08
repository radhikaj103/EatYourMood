// Getting location element from the html page
var x = document.getElementById("location");

function getLocation( )
{
  if( navigator.geolocation )
  {
      console.log(" >> Inside nav.geoloc if()");
      navigator.geolocation.getCurrentPosition( showPosition, logError );
  } 
  else
  {
    console.log(" >> Geolocation is not supported by browser");
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition( position )
{
    console.log(" >>showPosition called");
  x.innerHTML = 
    "Latitude: " + position.coords.latitude + 
    "<br/>" + "Longitude: " + position.coords.longitude;
}


function logError( positionError ) 
{
    console.log(positionError);
    x.innerHTML =  "Could not retrieve location: \"" + positionError.message + "\" \n Will show box to enter city they reside in";
}

getLocation();