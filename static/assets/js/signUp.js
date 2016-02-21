$(function(){
	//$('#btnSignUp').click(function(){
    //
	//	$.ajax({
	//		url: '/signUp',
	//		data: $('form').serialize(),
	//		type: 'POST',
	//		success: function(response){
	//			console.log(response);
	//		},
	//		error: function(error){
	//			console.log(error);
	//		}
	//	});
	//});

	$('#climateLoginButton').click(function(){
		var redirectUrl = encodeURIComponent(window.location.href);
		//KEEP THE STRING THE SAME
		redirectUrl=encodeURIComponent("http://127.0.0.1:5000/croptimize")
          window.location.href = 'https://www.climate.com/static/app-login/?mobile=true&client_id=dp1fms099lu374&redirect_uri=' + redirectUrl;
	});
});