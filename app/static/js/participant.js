$(function() {
    $("#donate_now").click(function() {
	$.ajax({
	    type: 'GET',
	    url: '/api/donate/' + $(this).attr("data-participant_id"),
	    success: function() {
		window.location.reload();
	    }
	});
    });
});
