/*
 * Entry point for the companion app
 */
export function FitpiApi() {
}

//----------------------HELPERS------------------------------------
var handleResponse = (response) => {
  return response.json().then((responseJson) => {
    console.log(JSON.stringify(responseJson));
    if (responseJson.success === false) {
      if (responseJson.errors) {
        return Promise.reject(Error(responseJson.errors[0].message));
      }
      return Promise.reject(Error(responseJson.message));
    }
    return responseJson;
  })
};
//---------------------------------------------------------------------

const NUTRITRION_STATS_URL = "";
const NUTRITION_MEAL_GET_URL = "";
const TIMETABLE_NEXT_CLASS_URL = ""; //?json=y&Hour=9&OneOrAll=One&Day=Tuesday
const WORKLOG_CURRENT_MONTH_URL = " " //2019-06
const WORKLOG_ADD_LOG_URL = ""; //{month}/{date}/{start}/{end}/{duration}

FitpiApi.prototype.loadMfpData = function() {
  return fetch(NUTRITRION_STATS_URL)
    .then(function(response) {
       return handleResponse(response);
    }).then(function(response) {
        var meals = [];
    
        response.forEach(meal => {
        var returnMeal = {
        calories: meal.calories ? meal.calories : 0,
        date: meal.date
      };
        //console.log(returnMeal);
        meals.push(returnMeal); 
    });
       //console.log(meals); 
        return meals;
    });
}

FitpiApi.prototype.loadMfpData = function() {
  return fetch(NUTRITRION_STATS_URL)
    .then(function(response) {
       return handleResponse(response);
    }).then(function(response) {
        var meals = [];
  
       //console.log(meals); 
        return meals;
    });
}


FitpiApi.prototype.scoreTask = function(id, direction) {
  return fetch(SCORE_TASK_URL + id + "/score/" + direction, {
    headers: { 'x-api-user': userId , 'x-api-key': apiToken},
    method: 'POST'
  }).then(function(response) {
    return handleResponse(response);
  });
}


FitpiApi.prototype.scoreSubTask = function(id, subId, direction) {
  console.log("https://habitica.com/api/v3/task/" + id + "/checklist/" + subId + "/score/" + direction);
  return fetch("https://habitica.com/api/v3/task/" + id + "/checklist/" + subId + "/score/" + direction, {
    headers: { 'x-api-user': userId , 'x-api-key': apiToken},
    method: 'POST'
  }).then(function(response) {
    return handleResponse(response);
  });
}