import document from "document";
import * as messaging from "messaging";
import { ListTile } from "./listtile";
import { ListDetailTile } from "./listdetailtile";
import { ListDetail } from "./taskdetail";
import { me } from "appbit";


import { FitpiUI } from "./ui.js";
import { FitpiMessages } from "./messages.js";
import { FitpiController } from "./controller.js";

let ui = new FitpiUI();
let messages = new FitpiMessages();
let controller = new FitpiController(ui, messages);

let root = document.getElementById('root');
let screenWidth = root.width;

let menu_UI = document.getElementById("menu-list");
let meals_menu_UI = document.getElementById("meal-list");
let budgets_menu_UI = document.getElementById("budget-list");
let budgets_transaction_UI = document.getElementById("budget-detail-list");
let timetable_UI = document.getElementById("timetable-detail");
let worklog_UI = document.getElementById("worklog-detail-list");

let mealTiles_UI = [];

for (let i = 0; i < 9; i++) {
    let mealTile_UI = meals_menu_UI.getElementById(`meal-${i}`);
    if (mealTile_UI) {
        mealTiles_UI.push(mealTile_UI);
    }
}

let budget_tiles_UI = [];

for (let i = 0; i < 9; i++) {
    let budget_tile_UI = budgets_menu_UI.getElementById(`budget-${i}`);
    if (budget_tile_UI) {
        budget_tiles_UI.push(budget_tile_UI);
    }
}
budget_tiles_UI.forEach((element, index) => {
    let touch = element.getElementById("budget-detail-button");
    touch.onclick = (evt) => {
        if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
            //Send object as JSON string to companion
            messaging.peerSocket.send("budgets/" + element.text.split(" ")[0]);
        }
    }
});


let budget_detail_tiles_UI = [];

for (let i = 0; i < 9; i++) {
    let budget_tile_UI = budgets_transaction_UI.getElementById(`budget-${i}`);
    if (budget_tile_UI) {
        budget_detail_tiles_UI.push(budget_tile_UI);
    }
}

let worklog_detail_list_UI = [];

for (let i = 0; i < 9; i++) {
    let log_UI = worklog_UI.getElementById(`worklog-${i}`);
    if (log_UI) {
        worklog_detail_list_UI.push(log_UI);
    }
}



let showMealList = function() {
    if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
        //Send object as JSON string to companion
        messaging.peerSocket.send("meals");
    }
}

let showBudgetMenu = function() {
    if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
        //Send object as JSON string to companion
        messaging.peerSocket.send("budgets");
    }
}

let showTimetable = function() {
    if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
        //Send object as JSON string to companion
        messaging.peerSocket.send("timetable");
    }
}

let showWeather = function() {
    if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
        //Send object as JSON string to companion
        messaging.peerSocket.send("weather");
    }
}

let showWorklog = function() {
    if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
        //Send object as JSON string to companion
        messaging.peerSocket.send("worklog");
    }
}


let menuItems_UI = menu_UI.getElementsByClassName("tile-list-item");
menuItems_UI.forEach((element, index) => {
    let touch = element.getElementById("menu-button");
    touch.onclick = (evt) => {
        if (index == 0) {
            console.log(`touched: ${index}`);
            showMealList();
        }

        if (index == 1) {
            console.log(`touched: ${index}`);
            showBudgetMenu();
        }

        if (index == 2) {
            console.log(`touched: ${index}`);
            showWorklog();
        }

        if (index == 3) {
            console.log(`touched: ${index}`);
            showTimetable();
        }

        if (index == 4) {
            console.log(`touched: ${index}`);
            showWeather();
        }
    }
});

let mealItems_UI = meals_menu_UI.getElementsByClassName("tile-list-item");
mealItems_UI.forEach((element, index) => {
    let touch = element.getElementById("meal-detail-button");
    touch.onclick = (evt) => {
        if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
            //Send object as JSON string to companion

            messaging.peerSocket.send("meals/" + element.text.substring(0, 10));
        }
    }
});

messaging.peerSocket.onmessage = evt => {

    if (evt.data.isMeal) {
        var transactions = []
        evt.data.meals.forEach((element, index) => {
            var meal = {}
            meal.calories = element.calories;
            meal.date = element.date;
            transactions.push(meal);
        });


        meals_menu_UI.style.display = "inline";
        menu_UI.style.display = "none";

        var i;
        for (i = 0; i < transactions.length; i++) {
            let message = transactions[i].date + "   " + transactions[i].calories + "/2751 cals";
            mealTiles_UI[i].text = message;
        };


        //console.log(evt.data.meals);
    }


    if (evt.data.isMealDetail) {
        var meal = {}
        meal.calories = evt.data.meal.calories;
        meal.carbohydrates = evt.data.meal.carbohydrates;
        meal.fat = evt.data.meal.fat;
        meal.protein = evt.data.meal.protein;
        meal.sugar = evt.data.meal.sugar;

        meals_menu_UI.style.display = "none";
        menu_UI.style.display = "none";

        document.getElementById("meal-detail").style.display = "inline";

        document.getElementById("meal-detail-calories").text = "Calories: " + meal.carbohydrates;
        document.getElementById("meal-detail-carbs").text = "Carbs: " + meal.calories;
        document.getElementById("meal-detail-fat").text = "Fat: " + meal.fat;
        document.getElementById("meal-detail-protein").text = "Protein: " + meal.protein;
        document.getElementById("meal-detail-sugar").text = "Sugar: " + meal.sugar;


        //console.log(evt.data.meals);
    }

    if (evt.data.isTimetable) {
        var nextClass = {}
        nextClass.name = evt.data.timetable.name;
        nextClass.teacher = evt.data.timetable.teacher;
        nextClass.type = evt.data.timetable.type;
        nextClass.location = evt.data.timetable.location;
        nextClass.hours = evt.data.timetable.hours;

        meals_menu_UI.style.display = "none";
        menu_UI.style.display = "none";

        document.getElementById("timetable-detail").style.display = "inline";

        document.getElementById("timetable-tile-name").text = "Name: " +  nextClass.name;
        document.getElementById("timetable-tile-teacher").text = "Teacher: " +  nextClass.teacher;
        document.getElementById("timetable-tile-type").text = "Type: " +  nextClass.type;
        document.getElementById("timetable-tile-location").text = "Location: " +  nextClass.location;
        document.getElementById("timetable-tile-hours").text = "Hours: " +  nextClass.hours;


        //console.log(evt.data.meals);
    }

    if (evt.data.isBudget) {
        var transactions = []
        evt.data.budgets.forEach((element, index) => {
            var budget = {}
            budget.name = element.name;
            budget.sum = element.sum;
            transactions.push(budget);
        });


        budgets_menu_UI.style.display = "inline";
        menu_UI.style.display = "none";

        var i;
        for (i = 0; i < transactions.length; i++) {
            let message = transactions[i].name + "   " + transactions[i].sum + " spent";
            budget_tiles_UI[i].text = message;
        };


        //console.log(evt.data.meals);
    }


    if (evt.data.isBudgetDetail) {
        var transactions = []
        evt.data.transactions.forEach((element, index) => {
            var transaction = {}
            transaction.name = element.name;
            transaction.amount = element.amount;
            transactions.push(transaction);
        });


        budgets_transaction_UI.style.display = "inline";
        budgets_menu_UI.style.display = "none";

        var i;
          
      for (i = 0; i < 9; i++) {
            budget_detail_tiles_UI[i].text = "";
        };
      
        for (i = 0; i < transactions.length; i++) {
            budget_detail_tiles_UI[i].text = "";
            let message = transactions[i].name + ":   " + transactions[i].amount + "lei";
            budget_detail_tiles_UI[i].text = message;
        };


        //console.log(evt.data.meals);
    }

    if (evt.data.isWeather) {
        var weather = {}
        weather.temperature = evt.data.weather.temperature;
        weather.humidity = evt.data.weather.humidity;

        meals_menu_UI.style.display = "none";
        menu_UI.style.display = "none";

        document.getElementById("weather-detail").style.display = "inline";

        document.getElementById("temperature").text = weather.temperature + "°C";
        document.getElementById("humidity").text =  weather.humidity + "%";

        //console.log(evt.data.meals);
    }

    if (evt.data.isWorklog) {
        var logs = []
        evt.data.worklog.forEach((element, index) => {
            var log = {}
            log.date = element.date;
            log.duration = element.duration;
            log.start = element.start;
            log.end = element.end;
            logs.push(log);
        });


        document.getElementById("worklog-detail-list").style.display = "inline";
        menu_UI.style.display = "none";

        var i;          
      for (i = 0; i < 9; i++) {
          worklog_detail_list_UI[i].text = "";
        };
      
        for (i = 0; i < logs.length; i++) {
            let message = logs[i].date + " : " + logs[i].duration;
            let hourMessage =  logs[i].start + " - " + logs[i].end;
            worklog_detail_list_UI[i].text = message;
        };


        //console.log(evt.data.meals);
    }

}

document.onkeypress = function(e) {
    console.log("Key pressed: " + e.key);
    e.preventDefault();
    if (e.key === "back") {
        if (document.getElementById("meal-detail").style.display == "inline") {
            document.getElementById("meal-detail").style.display = "none";
            meals_menu_UI.style.display = "inline";
            menu_UI.style.display = "none";
        } else {
            if (meals_menu_UI.style.display == "inline") {
                document.getElementById("meal-detail").style.display = "none";
                meals_menu_UI.style.display = "none";
                menu_UI.style.display = "inline";
            } else {
                if (budgets_transaction_UI.style.display == "inline") {
                    budgets_menu_UI.style.display = "inline";
                    budgets_transaction_UI.style.display = "none";
                } else {
                    if ( budgets_menu_UI.style.display == "inline") {
                        budgets_menu_UI.style.display = "none";
                        menu_UI.style.display = "inline";
                    } else {
                        if (timetable_UI.style.display == "inline") {
                          console.log("timetable")
                            timetable_UI.style.display = "none";
                            menu_UI.style.display = "inline";
                        } else {
                            if (document.getElementById("weather-detail").style.display == "inline") {
                                document.getElementById("weather-detail").style.display = "none";
                                menu_UI.style.display = "inline";
                            } else {
                                if(worklog_UI.style.display == "inline") {
                                    worklog_UI.style.display = "none";
                                    menu_UI.style.display = "inline";
                                } else {
                                  me.exit();
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}