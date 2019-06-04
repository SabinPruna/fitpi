export function ListDetail(view, screenWidth) {
  
  this.text = view.getElementById("text");
  this.bg = view.getElementById("task-background");
  
  this.setText = (text) => {
    this.text.text = text;
  };
  
  this.setColor = (color) => {
    this.bg.style.fill = color;
  };
}