//variables
let items = document.querySelectorAll('.item');
let currentIndex = 0;
let nextButton = document.getElementById('next-button');
let previousButton = document.getElementById('previous-button');

//display the current item and update the page number
function showCurrentItem()
{
	for (var i = 0; i < items.length; i++)
	{

		//display the item if it matches the current index
		if (i === currentIndex)
		{
			items[i].style.display = 'block';
		}
		else
		{
			items[i].style.display = 'none';
		}
	}

	//update the page number
	document.getElementById('page-number').textContent = 'Page ' + (currentIndex + 1);
}

//go to the next item
function goToNextItem()
{
	if (currentIndex < items.length - 1)
	{
		currentIndex++;

		//enable the previous button
		previousButton.disabled = false;
	}

	//disable the next button if we have reached the last item
	if (currentIndex === items.length - 1)
	{

		nextButton.disabled = true;
	}
	showCurrentItem();
}

//go to the previous item
function goToPreviousItem()
{
	if (currentIndex > 0)
	{
		currentIndex--;
		nextButton.disabled = false;
	}
	if (currentIndex === 0)
	{
		previousButton.disabled = true;
	}
	showCurrentItem();
}

//show the current item when the DOM is loaded
document.addEventListener('DOMContentLoaded', showCurrentItem);

//event listeners on previous and next items
previousButton.addEventListener('click', goToPreviousItem);
nextButton.addEventListener('click', goToNextItem);