import document from "document";
import { ListTile } from "./listtile";
import { ListDetailTile } from "./listdetailtile";
import { ListDetail } from "./taskdetail";

export function FitpiUI() {

  this.menu = document.getElementById("menu-list");
  this.mealList = document.getElementById("meal-list");
  //this.detail = document.getElementById("meal-detail-list");

  this.root = document.getElementById('root');
  this.screenWidth = this.root.width;
  
  this.mealTiles = [];
  this.mealDetailTiles = [];
  
  for (let i = 0; i < 20; i++) {
    let mealTile = this.mealList.getElementById(`meal-${i}`);
    if (mealTile) {
        this.mealTiles.push(new ListTile(mealTile));
    }
  }
  
  //this.detailHolder = new ListDetail(this.detail, this.screenWidth);

  
  

FitpiUI.prototype.showMenu = function() {
  this.taskList.style.display = "none";
  this.menu.style.display = "inline";
  this.detail.style.display = "none";
}

FitpiUI.prototype.menuClicks = function(onClick) {
  var self = this;
  this.menu.onclick = function(e) {
    onClick(self.menu.value);
  }
}

}
