var feedback = function(res) {
    if (res.success === true) {
        var get_link = res.data.link.replace(/^http:\/\//i, 'https://');
        document.querySelector('.status').classList.add('bg-success');
        document.querySelector('.img').innerHTML =
			'<div class="uploaded-img" style="background-image:url(\''
			+ get_link +
			'\')"></div><h2 class="looks-great animated rubberBand">Looks great!</h2>';
		document.querySelector('.test').innerHTML = get_link;
		document.querySelector('.dropzone').classList.add('hidden');
		document.getElementById('pic_button').classList.add('post-upload-button');
    }
};

new Imgur({
    clientid: 'a3d4585229afb71', //You can change this ClientID
    callback: feedback
});