import * as messaging from "messaging";
import { inbox } from "file-transfer";
import * as fs from "fs";

export function FitpiMessages() {
  
  FitpiMessages.prototype.messages = function(onMeals) {
    messaging.peerSocket.onopen = function() {
    }

    messaging.peerSocket.onmessage = function(evt) {
      console.log(evt);
      console.log(evt.meals);
      if (evt.data.meals) {
        onMeals(evt.data.rewards)
      } else {
        onMeals(evt.data.message)
      }
    }
  }
  
  FitpiMessages.prototype.getSocket = function() {
    return new Promise(function(resolve, reject) {
      if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
        resolve(messaging.peerSocket);
      } else {
        reject();
      }
    });
  }
}