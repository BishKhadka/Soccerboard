//constants
const startContainer = document.querySelector('.start-container');
const infoContainer = document.querySelector('.info-container');
const quizContainer = document.querySelector('.quiz-container');
const resultContainer = document.querySelector('.result-container');
const playNowButton = startContainer.querySelector('.buttons .play-now');
const infoStartButton = infoContainer.querySelector('.buttons .start');
const infoQuitButton = infoContainer.querySelector('.buttons .quit');
const quizNextButton = quizContainer.querySelector('.buttons .next');
const resultReplayButton = resultContainer.querySelector('.buttons .replay');
const questionLineWidth = quizContainer.querySelector('.outer-box .inner-box');
const rulesList = infoContainer.querySelector('.rules-list');
const quitButtons = document.querySelectorAll('.quit');

//some variables
let totalQuestionsPlayed;
let totalScore;
let totalTimeGiven = 15;
let totalQuizQuestions = 10;
let tickIconHTML = '<div class="icon tick"><i class="fas fa-check"></i></div>';
let crossIconHTML = '<div class="icon cross"><i class="fas fa-times"></i></div>';
const totalQuestionsOnFile = questions.length;
let usedQuestions;
let timer;
let currQsnIdx;

//make play nw button visible

playNowButton.classList.add('button-enabled');

//gives a random unused question number 
function getRandomQuestionNumber() {
	let randomNum;
	randomNum = Math.floor(Math.random() * totalQuestionsOnFile)
	while (usedQuestions.has(randomNum)) {
		randomNum = Math.floor(Math.random() * totalQuestionsOnFile)
	}
	usedQuestions.add(randomNum);
	return randomNum;
}

//displays the information box
playNowButton.addEventListener('click', function() {

	//remove the current buttons and display and show guidelines box
	playNowButton.classList.remove('button-enabled');
	startContainer.classList.add('start-disabled');
	infoContainer.classList.add('info-enabled');
	infoStartButton.classList.add('button-enabled');
	infoQuitButton.classList.add('button-enabled');

    //add general information about the quiz game
	rulesList.innerHTML = '<span class = "rules">1. Total Questions: ' + totalQuizQuestions + '</span>' +
		'<span class = "rules">2. Time Limit: ' + totalTimeGiven + ' sec for each question </span>' +
		'<span class = "rules">3. Once you select an option, it cannot be changed.</span>' +
		'<span class = "rules">4. Once the quiz begins, there is no option to quit.</span>' +
		'<span class = "rules">5. There is no penalty for incorrect answers.</span>';
});

//starts the quiz 
infoStartButton.addEventListener('click', function() {

	totalQuestionsPlayed = 1;
	totalScore = 0;
	usedQuestions = new Set();
	quizNextButton.innerHTML = "Next";
	questionLineWidth.style.width = '0';

	infoContainer.classList.remove('info-enabled');
	infoStartButton.classList.remove('button-enabled');
	infoQuitButton.classList.remove('button-enabled');

	quizContainer.classList.add('quiz-enabled');

	//reset timer if there is one going on
	if (timer){
		stopCountdown();
	}

	createQuiz()
	startCountdown()

});

//function to handle quit button
function handleQuitClick(event) {
	window.location.reload();
	let currentURL = window.location.href;
    let newURL = currentURL.replace('/quiz', '');
    window.location.href = newURL;
  }
  
//when quit is clicked, it calls handleQuitClick and takes to the main page
quitButtons.forEach(function(button) {
	button.addEventListener('click', handleQuitClick);
  });

//displays the next quiz question
quizNextButton.addEventListener('click', function() {
	quizNextButton.classList.remove('button-enabled');
	if (quizNextButton.innerHTML == "Next") {
		quizContainer.querySelector('.option-list').innerHTML = "";
		createQuiz()
		startCountdown()

	} else if (quizNextButton.innerHTML == "Finish") {
		stopCountdown()
		showResult()
	}
});

//displays the result of the quiz
resultReplayButton.addEventListener('click', function() {
	resultContainer.classList.remove('result-enabled');
	resultReplayButton.classList.remove('button-enabled');

	document.querySelector('.result-container .quit').classList.remove('button-enabled');

	//reset timer if there is one before replay quiz
	if (timer){
		stopCountdown();
	}

	infoStartButton.dispatchEvent(new Event('click'));
});


//creates the quiz 
function createQuiz() {
	currQsnIdx = getRandomQuestionNumber()

    //question header display
	let questionNumberTag = quizContainer.querySelector('.quiz-heading .question-number');
	questionNumberTag.innerHTML = '<p>' + totalQuestionsPlayed + '/' + totalQuizQuestions + '</p>';

    //add the question to question box
	let questionTag = quizContainer.querySelector('.question-box .question');
	questionTag.innerHTML = questions[currQsnIdx].question;

    //add options to the optionlist
	let optionList = quizContainer.querySelector('.option-list');
	quizContainer.querySelector('.option-list').innerHTML = "";

	//creating shuffle indices to later shuffle the options
	arr = shuffleArray([0,1,2,3])

	//create options
	optionList.innerHTML += '<span class = "option" onclick = "checkClicked(this)">' + questions[currQsnIdx].options[arr[0]] + '</span>';
	optionList.innerHTML += '<span class = "option" onclick = "checkClicked(this)">' + questions[currQsnIdx].options[arr[1]] + '</span>';
	optionList.innerHTML += '<span class = "option" onclick = "checkClicked(this)">' + questions[currQsnIdx].options[arr[2]] + '</span>';
	optionList.innerHTML += '<span class = "option" onclick = "checkClicked(this)">' + questions[currQsnIdx].options[arr[3]] + '</span>';

	
}

//disable all other option and show the correct answer when an option is clicked
function checkClicked(selectedOption) {

    //pause the counter animation if an option is clicked
	document.querySelector('svg circle').style.animationPlayState = 'paused';
	stopCountdown();
	questionLineWidth.style.width = (totalQuestionsPlayed / totalQuizQuestions) * 100 + '%';

    //check if user answer is right
	let userAnswer = selectedOption.innerText;
	if (userAnswer == questions[currQsnIdx].answer) {
		totalScore += 1;
		selectedOption.classList.add("correct-ans");
		selectedOption.insertAdjacentHTML('beforeend', tickIconHTML);

	} else {
		selectedOption.classList.add("incorrect-ans");
		selectedOption.insertAdjacentHTML('beforeend', crossIconHTML);
		showCorrectAnswer()
	}

    //make options unclickable
	disableOptions()
	totalQuestionsPlayed += 1;
}

//makes all options unclickable
function disableOptions() {
	let allAnswerOptions = quizContainer.querySelectorAll('.option');

	allAnswerOptions.forEach((eachOption) => {
		eachOption.classList.add('pointer-events-disabled');
	});

    //change the text of Next to Finish after last question
	if (totalQuestionsPlayed == totalQuizQuestions) {
		quizNextButton.innerHTML = "Finish";
	}
	quizNextButton.classList.add('button-enabled');

}

//displays the correct answer option
function showCorrectAnswer() {
	let allAnswerOptions = quizContainer.querySelectorAll('.option');
	allAnswerOptions.forEach((eachOption) => {
		if (eachOption.innerText == questions[currQsnIdx].answer) {
			eachOption.classList.add("correct-ans");
			eachOption.insertAdjacentHTML('beforeend', tickIconHTML);
		}
	});
}

//displays the result of the quiz
function showResult() {

    //only display the result-container
	quizContainer.classList.remove('quiz-enabled');
	quizNextButton.classList.remove('button-enabled');

	resultContainer.classList.add("result-enabled");
	resultReplayButton.classList.add('button-enabled');
	document.querySelector('.result-container .quit').classList.add('button-enabled');
	
	const resultIconContainer = resultContainer.querySelector(".icon-container");
	const scoreText = resultContainer.querySelector(".result-score");
	let insertIconHTML = '';
	let insertScoreHTML = '';

    //if user scores very high in the quiz 
	if (totalScore >= Math.floor(0.8 * totalQuizQuestions)) {

        //three stars
		insertIconHTML = '<div class="star"><i class="fas fa-star"></i></div>' +
			'<div class="star"><i class="fas fa-star"></i></div>' +
			'<div class="star"><i class="fas fa-star"></i></div>';
		randomNum = Math.floor(Math.random() * threeStarHTMLTags.length)

        //add a quiz end comment
		insertScoreHTML = threeStarHTMLTags[randomNum] +
			'<span>Your final score is<p>' + totalScore + '</p>out of<p>' + totalQuizQuestions + '</p></span>';

		resultIconContainer.innerHTML = insertIconHTML;
		scoreText.innerHTML = insertScoreHTML;

    //if user gets good score in the quiz 
	} else if (totalScore >= Math.ceil(0.5 * totalQuizQuestions)) {

        //two stars
		insertIconHTML = '<div class="star"><i class="fas fa-star"></i></div>' +
			'<div class="star"><i class="fas fa-star"></i></div>';

		randomNum = Math.floor(Math.random() * twoStarHTMLTags.length)

        //add a quiz end comment
		insertScoreHTML = twoStarHTMLTags[randomNum] +
			'<span>Your final score is<p>' + totalScore + '</p>out of<p>' + totalQuizQuestions + '</p></span>';

		resultIconContainer.innerHTML = insertIconHTML;
		scoreText.innerHTML = insertScoreHTML;

    //if user does poor in the quiz
	} else {

        //one star
		insertIconHTML = '<div class="star"><i class="fas fa-star"></i></div>';
		randomNum = Math.floor(Math.random() * oneStarHTMLTags.length)

        //add a quiz end comment
		insertScoreHTML = oneStarHTMLTags[randomNum] +
			'<span>Your final score is<p>' + totalScore + '</p>out of<p>' + totalQuizQuestions + '</p></span>';
		resultIconContainer.innerHTML = insertIconHTML;
		scoreText.innerHTML = insertScoreHTML;
	}
}

//starts the countdown after each question is displayed
function startCountdown() {
	totalTimeGiven = 15;
	restartAnimation()
	let countdownNumberClass = quizContainer.querySelector('.countdown-number');
	countdownNumberClass.textContent = totalTimeGiven;
	timer = setInterval(function() {
		totalTimeGiven--;

        //stop the timer after timeout
		if (totalTimeGiven <= 0) {
			totalTimeGiven = 0;
			stopCountdown();

			document.querySelector('svg circle').style.animationPlayState = 'paused';
			disableOptions()
			showCorrectAnswer()
			quizContainer.querySelector('.buttons .next').classList.remove('next-disabled');
		}
		countdownNumberClass.textContent = totalTimeGiven;
	}, 1000);
}

//stops the countdown
function stopCountdown() {
	clearInterval(timer);
}

//restart the countdown animation
function restartAnimation() {
	let circle = document.querySelector("circle");
	var newCircle = circle.cloneNode(true);
	circle.parentNode.replaceChild(newCircle, circle);
	newCircle.style.animation = 'countdown 15s linear infinite forwards';
}

//Fisher-Yates shuffle algorithm
function shuffleArray(arr){
	for (let i = arr.length-1; i >0; i--){
		const j = Math.floor(Math.random() * (i + 1));
		const temp = arr[i];
	  	arr[i] = arr[j];
	  	arr[j] = temp;
	}
	return arr;
}

