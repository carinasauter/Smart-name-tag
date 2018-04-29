
$( ".reset" ).click(function() {
	$.ajax({
		url: "/resetInfo"
	});
});

$(document).ready(function(){
	$('.sidenav').sidenav();
});


// var interests = [];
$('.interest').css('cursor', 'pointer');
// // $('.interest').css('opacity', '0.6');


// $( document ).ready(function() {
//     var interestFields = document.getElementsByClassName("interest");
//     console.log(interestFields);
// });

// $( ".interest" ).click(function() {
//     var interestName = $(this).attr("interest");
//     if (interests.includes(interestName)) {
//         $(this).css("opacity", '0.6');
//         interests.pop(interestName);
//     } else {
//         interests.push(interestName);
//         $(this).css("opacity", '1');
//     }
//     console.log(my_interests);

//     $.ajax({
//         type: "POST",
//         data: {int: JSON.stringify(interests)},
//         url: "/updateInterests",
//         dataType: "json"
//     });
// });