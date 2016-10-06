var components = {
    carousel_w_thumbnails: '<h4>Carousel With Thumbnails</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component carousel_w_thumbs"><button class="btn btn-default select_gallery">Select Gallery</button><input class="hidden gallery_slug" name="components[{{ id }}].gallery" /><input class="hidden" name="components[{{ id }}].type" value="carousel_w_thumbnails" /></div></div>',
    carousel: '<h4>Carousel</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component carousel"><button class="btn btn-default select_gallery">Select Gallery</button><input class="hidden gallery_slug" name="components[{{ id }}].gallery" /><input class="hidden" name="components[{{ id }}].type" value="carousel" /></div></div>',
    info_carousel: '<h4>Carousel</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component carousel"><button class="btn btn-default select_gallery">Select Gallery</button><input class="hidden gallery_slug" name="components[{{ id }}].gallery" /><input class="hidden" name="components[{{ id }}].type" value="info_carousel" /></div></div>',
    banner: '<h4>Banner</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component banner"><button class="btn btn-default select_link">Select Link</button><button class="btn btn-default select_gallery">Select Gallery</button><input class="link" name="components[{{ id }}].link" /><input class="hidden gallery_slug" name="{{ id }}.gallery" /><textarea data-provide="markdown" class="form-control" name="components[{{ id }}].text" placeholder="Optional text to go above the banner. If the image for the background has text leave this blank." rows="5"></textarea><button class="btn btn-default link_page">Link Content From Page</button><input class="linked_slugs hidden" name="components[{{ id }}].linked_slugs" /><input class="hidden" name="components[{{ id }}].type" value="banner" /></div>',
    two_texts: '<h4>Banner</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component banner"><div class="row"><div class="col-xs-6"><textarea data-provide="markdown" class="form-control " name="components[{{ id }}].text" placeholder="First Text Column." rows="6"></textarea><input class="hidden" name="components[{{ id }}].type" value="two_texts" /></div><div class="col-xs-6"><textarea data-provide="markdown" class="form-control " name="components[{{ id }}].second_text" placeholder="Second Text Column." rows="6"></textarea></div></div></div>',
    four_headed: '<h4>Banner</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component banner"><div class="row"><div class="col-xs-6"><button class="btn btn-default select_link">Select Link</button><input class="link" name="components[{{ id }}].link" /><input class="form-control" name="components[{{ id }}].title" /><textarea data-provide="markdown" class="form-control " name="components[{{ id }}].text" placeholder="First Text Column." rows="6"></textarea><input class="hidden" name="components[{{ id }}].type" value="four_headed" /></div><div class="col-xs-6"><input class="form-control" name="components[{{ id }}].second_title" /><textarea data-provide="markdown" class="form-control " name="components[{{ id }}].second_text" placeholder="Second Text Column." rows="6"></textarea></div><div class="col-xs-6"><input class="form-control" name="components[{{ id }}].third_title" /><textarea data-provide="markdown" class="form-control " name="components[{{ id }}].third_text" placeholder="Second Text Column." rows="6"></textarea></div><div class="col-xs-6"><input class="form-control" name="components[{{ id }}].fourth_title" /><textarea data-provide="markdown" class="form-control " name="components[{{ id }}].fourth_text" placeholder="Fourth Text Column." rows="6"></textarea></div></div></div>',
    half_carousel: '<h4>Half Carousel</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component half_carousel"><div class="row"><div class="col-xs-12 col-sm-6"><button class="btn btn-default select_link">Select Link</button><button class="btn btn-default select_gallery">Select Gallery</button><input class="hidden gallery_slug" name="components[{{ id }}].gallery" /><input class="link" name="components[{{ id }}].link" /></div><div class="col-sm-6 col-xs-12"><textarea class="form-control" data-provide="markdown" rows="10" name="components[{{ id }}].text" placeholder="Add text here ..."></textarea><button class="btn btn-default link_page">Link Content From Page</button><input class="linked_slugs hidden" name="components[{{ id }}].linked_slugs" /><input class="hidden" name="components[{{ id }}].type" value="half_carousel" /></div></div></div></div>',
    reverse_half_carousel: '<h4>Right Half Carousel</h4><div class="col-xs-12" id="{{ id }}"><div class="proto_component half_carousel"><div class="row"><div class="col-sm-6 col-xs-12"><textarea class="form-control" data-provide="markdown" rows="10" name="components[{{ id }}].text" placeholder="Add text here ..."></textarea><button class="btn btn-default link_page">Link Content From Page</button><input class="linked_slugs hidden" name="components[{{ id }}].linked_slugs" /><input class="hidden" name="components[{{ id }}].type" value="reverse_half_carousel" /></div><div class="col-xs-12 col-sm-6"><button class="btn btn-default select_link">Select Link</button><button class="btn btn-default select_gallery">Select Gallery</button><input class="hidden gallery_slug" name="components[{{ id }}].gallery" /><input class="link" name="components[{{ id }}].link" /></div></div></div>'
}
    
var unique_id = 0;
var carousel_id = null;

$(function() {
    $("#submit_page").click(function() {
	var data = form2js("dynamic_page_form");
	$.ajax({
	    type: 'POST',
	    url: "/add_dynamic_page?section=" + getParameterByName("section"),
	    data: JSON.stringify(data),
	    contentType: 'application/json',
	    success: function(redirect) {
		window.location.href = redirect;
	    }
	});
    });
    $(".component_choice").click(function() {
	var type = $(this).attr("data-type");
	$("#dynamic_page_layout").append(NunjucksEnv.renderString(components[type], {id: unique_id + 1}));
	$('textarea[data-provide="markdown"]').markdown();
	unique_id = unique_id + 1;
	$("#add_component_modal").modal("hide");
	$(".select_link").unbind("click");
	$(".select_link").click(function(e) {
	    e.preventDefault();
	    $("#add_link_modal").modal('show');
	    carousel_id = this;
	});
	$("#link_selector_wrapper a").click(function() {
	    $("#link_holder").val($(this).attr("data-value"));
	});
	$("#add_link_selector_wrapper a").click(function() {
	    $("#add_link_holder").val($(this).attr("data-value"));
	    $("#add_link_selected_path").text($(this).attr("data-path"));
	});
	$("#choose_link").unbind("click");
	$("#choose_link").click(function(e) {
	    e.preventDefault();
	    $(carousel_id).parent().children('input.link').val($("#link_holder").val());
	    $("#add_link_holder").val("");
	    $("#add_link_modal").modal("hide");
	});
	$("#choose_add_link").unbind("click");
	$("#choose_add_link").click(function(e) {
	    e.preventDefault();
	    $(carousel_id).parent().children('input.linked_slugs').val($("#add_link_holder").val());
	    $("#add_link_holder").val("");
	    $("#link_page").modal("hide");
	});
	$(".link_page").unbind("click");
	$(".link_page").click(function(e) {
	    e.preventDefault();
	    $("#link_page").modal("show");
	    carousel_id = this;
	});
	$(".select_gallery").unbind("click");
	$(".select_gallery").click(function(e) {
	    e.preventDefault();
	    $("#select_gallery_modal").modal("show");
	    carousel_id = this;
	    $(".existing_gallery").click(function() {
		handle_gallery_selected(this)
	    });
	    $(".add_new_gallery_trigger").click(function() {
		$("#new_gallery_modal").modal("show");
	    });
	});

    })
});

function handle_gallery_selected(element) {
    var gallery_slug = $(element).attr("data-slug");
    $(".existing_gallery").unbind("click");
    $.ajax({
	type: 'GET',
	url: "/gallery/" + gallery_slug,
	contentType: "application/json",
	success: function(gallery) {
	    $(NunjucksEnv.renderString('<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3"><div class="gallery_select_block existing_gallery"><div class="gallery_select_img_wrapper"><img class="img-responsive height img-rounded center-block" src="{% if (g.images | length) > 0 %}{{ g.images[0].url }}{% else %}/static/img/No_image_available.svg{% endif %}" /> </div><h4 class="text-center">{{ g.title }}</h4></div></div>', {g: gallery})).appendTo($(carousel_id).parent());
	}
    });
    $(carousel_id).parent().children('input.gallery_slug').val(gallery_slug);
    $("#select_gallery_modal").modal('hide');
};
