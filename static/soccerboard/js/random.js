let importedArray = require('./questions.js');
// console.log(importedArray); // Output: [1, 2, 3, 4, 5]
const fs = require('fs');
// Output array
// const outputArray = questions;
// console.log()

// // Convert array to string

function shuffleArray(arr){
	for (let i = arr.length-1; i >0; i--){
		const j = Math.floor(Math.random() * (i + 1));
		const temp = arr[i];
	  	arr[i] = arr[j];
	  	arr[j] = temp;
	}
	return arr;
}

importedArray = shuffleArray(importedArray);
const arrayString = JSON.stringify(importedArray);





// // File path and name
const filePath = 'output.js'; 

// // Create the JavaScript file
fs.writeFileSync(filePath, `const outputArray = ${arrayString};`);

// console.log('Array saved to output.js');