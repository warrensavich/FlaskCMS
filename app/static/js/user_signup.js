$(document).ready(function() {
    $("#register_user_form").submit(function(event) {
	event.preventDefault();
	$.ajax({
	    type: 'POST',
	    url: '/api/new_user',
	    data: JSON.stringify(form2js("register_user_form")),
	    contentType: "application/json",
	    success: function() {
		alert("Success!");
		window.location.href = "/";
	    },
	    error: function() {
		alert("Error");
	    }
	});
    });
});
