$(document).ready(function() {

	var mybot = '<div class="chatCont" id="chatCont">'+
								'<div class="bot_profile">'+
								    '<span class="bot_p_text"> Food Bot</span>'+
									'<img src="./static/bot_img/welcome.jpg" class="bot_p_img">'+

									'<div class="close">'+
										'<i class="fa fa-times" aria-hidden="true"></i>'+
									'</div>'+
									'<div class="refresh" id="idReload"><i class="fa fa-refresh" aria-hidden="true"></i></div>'
                                    +
								'</div><!--bot_profile end-->'+

								'<div id="result_div" class="resultDiv conversation-part--animation"></div>'+
								'<div class="chatForm" id="chat-div">'+
									'<div class="spinner">'+
										'<div class="bounce1"></div>'+
										'<div class="bounce2"></div>'+
										'<div class="bounce3"></div>'+
									'</div>'+
									'<input type="text" id="chat-input" autocomplete="off" placeholder="Try typing here"'+ 'class="form-control bot-txt"/>'+
									'<pre id=\'send\'> </pre>' +
								'</div>'+
							'</div><!--chatCont end-->'+

							'<div class="profile_div">'+
								'<div class="row">'+
									'<div class="col-hgt">'+
										'<img src="./static/bot_img/welcome.jpg" class="img-circle img-profile">'+
									'</div><!--col-hgt end-->'+
									'<div class="col-hgt">'+
										'<div class="chat-txt">'+
											'Ask Tom !!'+
										'</div>'+
									'</div><!--col-hgt end-->'+
								'</div><!--row end-->'+
							'</div><!--profile_div end-->';

	$("mybot").html(mybot);

	// ------------------------------------------ Toggle chatbot -----------------------------------------------
	$('.profile_div').click(function() {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
		document.getElementById('chat-input').focus();
	});

	$('.close').click(function() {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
	});

});
//								'<div data="[object Object]"  class="sc-VigVT hThaFZ"><div class="sc-jTzLTM fzQDea"><div><div class="sc-chPdSV eRysRd"><span style="font-size: 25px;">Hello! <img src="//s3.amazonaws.com/sf-thomas-cook/chatsdk/v1/Hi9aaeed75526981073dcb1189dc5c98b6.png"> </span><br></div></div></div></div>'+
