$(document).ready(function() {
	// setInterval(function() {
	// 	$('.container').css('margin-top', screen.height / 2 - 200 + 'px');
	// }, 100);
	$('#success').hide();
	$('#alert').hide();
	var filename = '';
	$('#cv').change(function() {
		event.preventDefault();
		filename = $('#cv').val();
		filename = filename.replace(/^.*[\\\/]/, '');
		$('#cv-label').html(filename);
	});
	$('#submit').click(function() {
		event.preventDefault();
		if (filename !== '') {
			ext = filename.split('.');
			index = ext.length;
			ext = ext[index - 1];
			if (ext == 'pdf') {
				$.ajax({
					url: 'upload.php',
					type: 'POST',
					data: new FormData(document.getElementById('cv_form')),
					contentType: false,
					processData: false,
					success: function(data) {
						$('#cv-label').html('Choose file');
						$('#success').fadeIn();
						filename = '';
						setTimeout(function() {
							$('#success').fadeOut();
						}, 4000);
					}
				});
			} else {
				$('#alert').fadeIn();
				setTimeout(function() {
					$('#alert').fadeOut();
				}, 4000);
			}
		} else {
			$('#alert').fadeIn();
			setTimeout(function() {
				$('#alert').fadeOut();
			}, 4000);
		}
	});
});
