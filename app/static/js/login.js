$(document).ready(function() {
    $("#login").click(function() {
	$.ajax({
	    type: 'POST',
	    url: '/api/login'
	    data: JSON.stringify({
		email: $("#email").val(),
		password: $("#password").val()
	    }),
	    contentType: "application/json",
	    success: function() {
		window.location.href="/";
	    }
	});
    });
});
