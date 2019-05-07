export function FitPiApi() {
};

FitPiApi.prototype.weatherData = function() {
  let self = this;
  
  return new Promise(function(resolve, reject) {
    let url = "weather-url";
  
    fetch(url).then(function(response) {
      return response.json();
    }).then(function(json) {
      console.log("Got JSON response from server:" + JSON.stringify(json));
      let weatherData = json; //JSON.parse(json);
      
      console.log(typeof json)
      
      
      let mostRecentDate = new Date(Math.max.apply(null, weatherData.map( e => {
       return new Date(e.date);
      })));
      console.log("most recent date" + mostRecentDate)
      
      let mostRecentObject = weatherData.filter( e => { 
        var d = new Date( e.date ); 
        return d.getTime() === mostRecentDate.getTime();
      })[0];
      console.log("most recent object" + mostRecentObject)
      
      resolve(mostRecentObject);
    }).catch(function (error) {
      reject(error);
    });
  });
}