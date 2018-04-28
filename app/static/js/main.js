interests = [];

$(document).ready(function(){
    $('.sidenav').sidenav();
  });

$('.interest').css('cursor', 'pointer');

$('.interest').css('opacity', '0.6');


$( ".interest" ).click(function() {
	var interestName = $(this).attr("interest");
	if (interests.includes(interestName)) {
		$(this).css("opacity", '0.6');
		interests.pop(interestName);
	} else {
		interests.push(interestName);
		$(this).css("opacity", '1');
	}
	console.log(interests);

	$.ajax({
		type: "POST",
		data: {int: JSON.stringify(interests)},
		url: "/updateInterests",
		dataType: "json"
	});
});

