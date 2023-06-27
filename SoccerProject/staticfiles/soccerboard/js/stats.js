var items = document.querySelectorAll('.item');
var currentIndex = 0;

function showCurrentItem() {
  for (var i = 0; i < items.length; i++) {
    if (i === currentIndex) {
      items[i].style.display = 'block';
    } else {
      items[i].style.display = 'none';
    }
  }
  document.getElementById('page-number').textContent = 'Page ' + (currentIndex + 1);
}

function goToNextItem() {
  if (currentIndex < items.length - 1) {
    currentIndex++;
    previousButton.disabled = false; // Enable the "Previous" button when moving to the next item
  }
  if (currentIndex === items.length - 1) {
    nextButton.disabled = true; // Disable the "Next" button at the end of the loop
  }
  showCurrentItem();
}

function goToPreviousItem() {
  if (currentIndex > 0) {
    currentIndex--;
    nextButton.disabled = false; // Enable the "Next" button when going back to a previous item
  }
  if (currentIndex === 0) {
    previousButton.disabled = true; // Disable the "Previous" button at the beginning of the loop
  }
  showCurrentItem();
}

document.addEventListener('DOMContentLoaded', showCurrentItem);

var previousButton = document.getElementById('previous-button');
previousButton.addEventListener('click', goToPreviousItem);

var nextButton = document.getElementById('next-button');
nextButton.addEventListener('click', goToNextItem);
