//run the slideshow every 3000 ms (3 sec)
setInterval(function ()
{
	let activeSlide = document.querySelector('.carousel-item.active');

	//next slide is the sibling element or the first slide if there is no next sibling
	let nextSlide = activeSlide.nextElementSibling || document.querySelector('.carousel-item:first-child');

	//display the next slide
	activeSlide.classList.remove('active');
	nextSlide.classList.add('active');
}, 3000);