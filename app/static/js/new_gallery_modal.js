WorkingGallerySlug = null;
$(function() {
    $("#submit_new_gallery").click(function(event) {
	event.preventDefault();
	submit_new_gallery();
    });
    $("#done_adding_images").click(function(event) {
	event.preventDefault();
	$.ajax({
	    type: 'GET',
	    url: "/gallery/" + WorkingGallerySlug,
	    contentType: 'application/json',
	    success: function(gallery) {
		$(NunjucksEnv.renderString('<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3"><div class="gallery_select_block existing_gallery"><div class="gallery_select_img_wrapper"><img class="img-responsive img-rounded center-block" src="{% if (g.images | length) > 0 %}{{ g.images[0].url }}{% else %}/static/img/No_image_available.svg{% endif %}" /> </div><h4 class="text-center">{{ g.title }}</h4><input type="radio" class="gallery_select_input" value="{{ g.slug }}" name="gallery" /></div></div>', {g: gallery})).insertBefore($('.add_new_gallery_trigger').parent());
		$("#new_gallery_modal").modal('hide');
		$(".new_gallery_modal_title").html("Add New Gallery");
		$("#modal_gallery_title_holder").removeAttr("style");
		$("#added_images_holder").empty();
		$("#modal_image_uploader_holder").attr("style", "display:none");
		$('input[name="gallery_title"]').val("");
		WorkingGallerySlug = null;
		$(".existing_gallery").unbind("click");
		$(".existing_gallery").click(function() {
		    handle_gallery_selected(this);
		});
	    }
	});
    });
});

function submit_new_gallery() {
    $.ajax({
	type: 'POST',
	url: '/api/gallery',
	data: JSON.stringify({gallery_title: $('input[name="gallery_title"]').val()}),
	contentType: "application/json",
	success: function(gallery_slug) {
	    $(".new_gallery_modal_title").html($('input[name="gallery_title"]').val());
	    WorkingGallerySlug = gallery_slug;
	    $("#modal_gallery_title_holder").slideUp("fast");
	    $("#modal_image_uploader_holder").slideDown("fast");
	    $("#dropzone_for_images").dropzone({url: "/gallery/" + WorkingGallerySlug, 
						previewTemplate : '<div style="display:none"></div>',
						success: function(f, resp) {
						    $("#added_images_holder").append(NunjucksEnv.renderString('<div class="col-md-4 col-lg-4 col-sm-6 col-xs-12"><div class="added_image_wrapper"><div class="gallery_select_img_wrapper"><img class="img-responsive height center-block" src="{{ url }}" /></div><label>Title</label><input class="form-control" name="img_title" /><button class="btn btn-block update_title" data-img_id="{{ id }}">Update Title</button></div></div>', resp));
						    $(".update_title").unbind("click");
						    $(".update_title").click(function(e) {
							e.preventDefault();
							update_title(this);
						    });
						}
					       });
	}
    });
};

function update_title(element) {
    $.ajax({
	type: 'PUT',
	url: "/image/" + $(element).attr("data-img_id"),
	contentType: "application/json",
	data: JSON.stringify({title: $(element).parent().children('input[name="img_title"]').val()}),
	success: function() {
	    $(element).parent().append('<h5 class="text-success successful_title" style="display:none">Title Updated</h5>');
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
