$(function() {
    $("#add_tag_btn").click(function(e) {
	e.preventDefault();
	$.ajax({
	    type: 'POST',
	    url: '/api/tag',
	    contentType: 'application/json',
	    data: JSON.stringify({title: $("#add_tag_input").val()}),
	    success: function(tag) {
		$(".tag_container").append(NunjucksEnv.renderString('<div class="float-left tag_wrapper"><label><input type="checkbox" value="{{ t.slug }}" /> {{ t.title }}</label></div>', {t: tag}));
		$("#add_tag_modal").modal("hide");
		$("#add_tag_input").val("");
	    }
	});
    });
});
