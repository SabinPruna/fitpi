import * as messaging from "messaging";

export function FitpiController(ui, messages) {
  
  var state;
  var listIndex;
  const LIST_COLORS = [
    "#ffffff",
    "#993e76",
    "#4444AA",
    "#118811",
  ]

  let onTasks = data =>{
    tasks = data;
    if (state === "loading") {
      showTaskList(true, false);
    } else {
      showMenu();
    }
  }

  let onStatus = message => {
    console.log(message);
  }

  let onRewards = rewards => {
    console.log(rewards);
    ui.hideDetail();
    ui.showStatus(rewards);
    setTimeout(() => ui.hideStatus(), 2000);
  }
  
  let onMeals = meals => {
    console.log(meals);
    ui.hideMenu();
  }
 
  
  let showMealsList = function() {
    
  }
  
  
  //Listen to events
  ui.menuClicks(value => {
    listIndex = value;
    if(listIndex == 0) {
      showMealsList();
    }
    //showTaskList(true, true);
  });
  
  messages.messages(onMeals);
  

  
}