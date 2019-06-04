import { me } from "companion";
import * as messaging from "messaging";
import { settingsStorage } from "settings";

import { FitpiApi } from "./fitpi.js"

//---------------------HELPERS--------------------------
String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};

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

//------------------------------------------------------

console.log("Companion Started");

let fitpiApi = new FitpiApi();

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

//console.log(yyyy + "-" + mm);


settingsStorage.onchange = function(evt) {
    init();
}

messaging.peerSocket.onopen = function() {
    init();
    listenToMessages();
}

function init() {
    var meals = loadMeals();
};

function loadMeals() {
    return fitpiApi.loadMfpData();
};


function listenToMessages() {
    messaging.peerSocket.onmessage = function(evt) {
        console.log(JSON.stringify(evt.data));
        var data = evt.data;

        console.log("--------------")
        console.log(data);
        console.log("--------------")

        if (data == "meals") {
            //var meals = loadMeals();

            fetch("")
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
                }).then(function(response) {
                    console.log(response);
                    console.log({ isMeal: 1, meals: response });
                    messaging.peerSocket.send({ isMeal: 1, meals: response });
                });
        }

        //for detail meal
        if (data.includes("meals/")) {
            let url = "" + data.substring(5);
            console.log(url);
            fetch(url)
                .then(function(response) {
                    return handleResponse(response);
                }).then(function(response) {   
                    var returnMeal = {
                        calories: response.calories ? response.calories : 0,
                            carbohydrates: response.carbohydrates ? response.carbohydrates : 0,
                        fat: response.fat ? response.fat : 0,
                        protein: response.protein ? response.protein : 0,
                        sugar: response.sugar ? response.sugar : 0,
                           
                    };
                    console.log(returnMeal);

                    return returnMeal;
                }).then(function(response) {
                    console.log(response);
                    console.log({ isMealDetail: 1, meal: response });
                    messaging.peerSocket.send({ isMealDetail: 1, meal: response });
                });
        }

        if (data == "budgets") {
            //var meals = loadMeals();
            let url = "" + yyyy + "-" + mm;
            fetch(url)
                .then(function(response) {
                    return handleResponse(response);
                }).then(function(response) {
                    var budgets = [];

                    response.forEach(budget => {   
                        var returnedBudget = {
                            name: budget.name,
                            sum: budget.sum
                        };
                        //console.log(returnMeal);
                        budgets.push(returnedBudget);  
                    });
                    //console.log(meals); 
                    return budgets;
                }).then(function(response) {
                    console.log(response);
                    console.log({ isBudget: 1, budgets: response });
                    messaging.peerSocket.send({ isBudget: 1, budgets: response });
                });
        }

        if (data.includes("budgets/")) {
            //var meals = loadMeals();
            let name = data.substring(7);
            let url = "" + yyyy + "-" + mm  + name;
            console.log(url);
            fetch(url)
                .then(function(response) {
                    return handleResponse(response);
                }).then(function(response) {
                    var transactions = [];

                    response.forEach(trans => {   
                        var returnedTransaction = {
                            name: trans.name,
                            amount: trans.amount
                        };
                        //console.log(returnMeal);
                        transactions.push(returnedTransaction);  
                    });
                    //console.log(meals); 
                    return transactions;
                }).then(function(response) {
                    console.log(response);
                    console.log({ isBudgetDetail: 1, transactions: response });
                    messaging.peerSocket.send({ isBudgetDetail: 1, transactions: response });
                });
        }

        if (data == "timetable") {
            var today = new Date();
            var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

            var dayName = days[today.getDay()];

            console.log(dayName)    

            let url = "" + today.getHours() + "&OneOrAll=One&Day=" + dayName;
            console.log(url);
            fetch(url)
                .then(function(response) {
                    return handleResponse(response);
                }).then(function(response) {   
                    var returnedClass = {
                       name: response.Name,
                       teacher: response.Teacher,
                       type: response.Type,
                       location: response.Location,
                       hours: response.Hours
                           
                    };
              
                    if(returnedClass.type == "L") {
                      returnedClass.type = "Lab"
                    } else {
                       if(returnedClass.type == "C") {
                         returnedClass.type = "Course"
                       }
                    }
              
                    console.log(returnedClass);

                    return returnedClass;
                }).then(function(response) {
                    console.log(response);
                    console.log({ isTimetable: 1, timetable: response });
                    messaging.peerSocket.send({ isTimetable: 1, timetable: response });
                });
        }

        if (data == "weather") {
            let url = "";
            console.log(url);
            fetch(url)
                .then(function(response) {
                    return handleResponse(response);
                }).then(function(response) {   
                    var returnedWeather = {
                       temperature: response[0].temperature,
                       humidity: response[0].humidity,                   
                    };
                                        
                    console.log(returnedWeather);

                    return returnedWeather;
                }).then(function(response) {
                    console.log(response);
                    console.log({ isWeather: 1, weather: response });
                    messaging.peerSocket.send({ isWeather: 1, weather: response });
                });
        }

        if (data == "worklog") {
            let url = "" + yyyy + "-" + mm ;
            console.log(url);
            fetch(url)
                .then(function(response) {
                    return handleResponse(response);
                }).then(function(response) {   
                    var logs = [];

                    response.forEach(log => {   
                        var returnedTransaction = {
                            duration: log.duration,
                            date: log.date,
                            start: log.start,
                            end: log.end
                        };
                        //console.log(returnMeal);
                        logs.push(returnedTransaction);  
                    });
                    //console.log(meals); 
                    return logs;
                }).then(function(response) {
                    console.log(response);
                    console.log({ isWorklog: 1, worklog: response });
                    messaging.peerSocket.send({ isWorklog: 1, worklog: response });
                });
        }

    }
}
//---------------HELPERS------------------------------

function handleError(error) {
    messaging.peerSocket.send({ message: error.message });
}