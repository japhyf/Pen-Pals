var feedback = function(res) {
    if (res.success === true) {
        var get_link = res.data.link.replace(/^http:\/\//i, 'https://');
        document.querySelector('.status').classList.add('bg-success');
        document.querySelector('.img').innerHTML =
            '<img src="' + get_link + '" height="250px" width="250px"/>';
		document.querySelector('.test').innerHTML = get_link;
		document.querySelector('.dropzone').classList.add('hidden');
    }
};

new Imgur({
    clientid: 'a3d4585229afb71', //You can change this ClientID
    callback: feedback
});