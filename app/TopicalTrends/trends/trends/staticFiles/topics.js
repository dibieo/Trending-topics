/**
* Makes an ajax call for hot trends on change of a select option.
*/

$(document).ready(function() {
 
$(".sort").change(function() {
var input = $(this).val();
$("#freqtopics").html("<div>Loading ...</div>");
$.get("/ui/topics?sort=" + input, function(data){
  $("#freqtopics").html(data);
});
})
});
