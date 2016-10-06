$(function() {
    $(".existing_gallery").click(function() {
	$(this).find('input[name="gallery"]').prop("checked", true);
    });
    $(".add_new_gallery_trigger").click(function() {
	$("#new_gallery_modal").modal("show");
    });
});

function handle_gallery_selected(element) {
    $(element).find('input[name="gallery"]').prop("checked", true);
}
