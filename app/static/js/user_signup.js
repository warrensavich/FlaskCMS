$(document).ready(function() {
    $("#sign_up").click(function() {
	var data = $("#new_user_form").serializeArray();
	data.roles = ["user", "seeker"];
	$.ajax({
	    type: 'POST',
	    url: '/register',
	    data: JSON.stringify(data),
	    contentType: "application/json",
	    success: function() {
		alert("Success");
	    },
	    error: function() {
		alert("Error");
	    }
	});
    });
});
