
$( ".reset" ).click(function() {
	$.ajax({
		url: "/resetInfo"
	});
});


$('.interest').css('cursor', 'pointer');


$(document).ready(function(){
    $('.sidenav').sidenav();
  });


var instance = M.Sidenav.getInstance(elem);
console.log(instance);