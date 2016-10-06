var current_btn = null;
$(function() {
    $(".delete_image").click(function(e) {
	$.ajax({
	    type: 'DELETE',
	    url: $(this).attr('data-url'),
	    success: function() {
		window.location.reload();
	    }
	});
    });
    $(".update_title").click(function(e) {
	e.preventDefault();
	update_title(this);
    });
    $(".link_trigger").click(function(e) {
	e.preventDefault();
	current_btn = this;
	$("#add_link_modal").modal('show');
    });
    $("#choose_link").click(function(e) {
	e.preventDefault();
	$(current_btn).parents(".input-group").children('input.link').val($("#link_holder").val());
	console.log($("#link_holder").val())
	$("#link_holder").val("");
	$("#add_link_modal").modal("hide");
    });
    $("#link_selector_wrapper a").click(function() {
	$("#link_holder").val($(this).attr("data-value"));
    });
    $("#dropzone_for_images").dropzone({url: window.location.href,
					previewTemplate : '<div style="display:none"></div>',
					success: function(f, resp) {
					    $("#added_images_holder").append(NunjucksEnv.renderString('<div class="col-md-4 col-lg-4 col-sm-6 col-xs-12"><a class="close delete_image" aria-label="Delete" data-url="/image/{{ id }}"><span aria-hidden="true">&times;</span></a><div class="added_image_wrapper"><div class="gallery_select_img_wrapper"><img class="img-responsive height center-block" src="{{ url }}" /></div><label>Link</label><div class="input-group"><input type="text" class="form-control link" name="img_link"><span class="input-group-btn"><button class="btn btn-default link_trigger" type="button"><i class="fa fa-search"></i></button></span></div><label>Title</label><input class="form-control" name="img_title" /><button class="btn btn-block update_title" data-img_id="{{ id }}">Update Image</button></div></div>', resp));
					    $(".update_title").unbind("click");
					    $(".update_title").click(function(e) {
						e.preventDefault();
						update_title(this);
					    });
					    $(".link_trigger").unbind("click");
					    $(".link_trigger").click(function(e) {
						e.preventDefault();
						current_btn = this;
						$("#add_link_modal").modal('show');
					    });
					    $(".delete_image").click(function(e) {
						$.ajax({
						    type: 'DELETE',
						    url: $(this).attr('data-url'),
						    success: function() {
							window.location.reload();
						    }
						});
					    });
					}
				       });
});

function update_title(element) {
    $.ajax({
	type: 'PUT',
	url: "/image/" + $(element).attr("data-img_id"),
	contentType: "application/json",
	data: JSON.stringify({title: $(element).parent().children('input[name="img_title"]').val(), link: $(element).parent().find('input[name="img_link"]').val(), alt_text: $(element).parent().find('textarea[name="alt_text"]').val()}),
	success: function() {
	    $(element).parent().append('<h5 class="text-success successful_title" style="display:none">Image Updated</h5>');
	    $(element).parent().children('.successful_title').slideDown("slow", function() {
		setTimeout(function() {
		    $(element).parent().children('.successful_title').slideUp("slow", function() {
			$(this).remove();
		    });
		}, 3000);
	    });
	}
    });
};
