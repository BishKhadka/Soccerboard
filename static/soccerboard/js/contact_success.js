//constants
const gif = document.getElementById('gif');

//reloads the GIF
function reloadGIF()
{
	const src = gif.getAttribute('src');

	//clear the 'src' attribute
	gif.setAttribute('src', '');

	//set 'src' attribute to its original value (reloads)
	gif.setAttribute('src', src);
}

//event listener for the 'load' event
window.addEventListener('load', function ()
{
	reloadGIF();

	//timeout function
	setTimeout(function ()
	{
		let text = document.querySelector('.land');
		text.classList.remove('disabled');
		gif.style.display = 'none';
	}, 1900);
});