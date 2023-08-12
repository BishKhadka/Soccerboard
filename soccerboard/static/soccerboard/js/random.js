let importedArray = require("./questions.js");
const fs = require("fs");

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
  }
  return arr;
}

importedArray = shuffleArray(importedArray);
const arrayString = JSON.stringify(importedArray);

const filePath = "output.js";

fs.writeFileSync(filePath, `const outputArray = ${arrayString};`);
