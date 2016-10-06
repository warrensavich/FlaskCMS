var NunjucksEnv;
$(function() {
    NunjucksEnv = new nunjucks.Environment(new nunjucks.WebLoader('/static/templates', { autoescape: true }));
    $('#login').popover({
	html: true,
	content: '<form id="login_form"><input class="form-control" name="email" placeholder="Email"><input class="form-control" placeholder="Password" type="password" name="password"></form><button class="btn btn-primary btn-block" id="login_btn">Submit</button>',
	placement: "bottom",
	title: "Log In",
	trigger: "click"
    });
    $("#login").on('shown.bs.popover', function() {
	$("#login_btn").click(function() {
	    $.ajax({
		type: 'POST',
		url: '/api/login',
		data: JSON.stringify(form2js("login_form")),
		contentType: "application/json",
		success: function() {
		    window.location.reload();
		}
	    });
	});
    });
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
