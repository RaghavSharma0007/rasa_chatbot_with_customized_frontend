
var uid = document.getElementById("myVar").value;
var socket = new WebSocket('ws://' + window.location.host + '/ws/chat/' +uid + '/');
var loaderHTMl="<div class='typing_loader'><div class='conversation-part conversation-part--question'><div class='avatar-wrapper same-row'><div class='avatar'></div></div><div class='same-row question-part text-ltr'><div class='bubble no-border' style='display: table; direction: unset;'><div class='bubble-label'><div class='ticontainer'><div class='tiblock'><div class='tidot'></div><div class='tidot'></div><div class='tidot'></div></div></div></div></div></div></div></div>"

function onButtonClick(mess_1) {
    var payload = mess_1['payload'];
    var input1 = mess_1['title'];
    if (payload) {
    socket.send(JSON.stringify({
    "message":payload,
    "type":"user_uttered"
    }))
     var html1="<div class='conversation-part conversation-part--answer'><div class='answer text-ltr'><div class='bubble no-border theme-background'><div class='bubble-label-answer'>"+input1+"</div></div>"+"<span class='comment' data-timestamp='"+moment().format("YYYY-MM-DD HH:mm:ss.SSS")+"'>just now</span>"+"</div></div>"
	 $("#result_div").append(html1);
     $("#chat-input").val('');
     $('div.option-wrapper').remove();
      $('#result_div').animate({scrollTop: $('#result_div').get(0).scrollHeight},1000);
    $('#result_div').append(loaderHTMl);
    }
  }

//window.onload = function() { }

function updateTimeStamps() {

    const elements = document.querySelectorAll(".comment");
    for(var i = 0; i < elements.length; i++){
        var timestamp=elements[i].dataset.timestamp;
        if (timestamp ){
        elements[i].textContent=moment(timestamp).fromNow();
        }

    }
 }



$(document).ready(function() {
    moment.relativeTimeThreshold('ss', 0);
    setInterval(updateTimeStamps, 5000);

	function appendBotMessage(data) {

       var arrayOfObjects=data['message']

        var appendHTML=""
         for (var i = 0; i < arrayOfObjects.length; i++) {

              if (i==0){
                  var innerHtml="<div class='conversation-part conversation-part--question'><div class='avatar-wrapper same-row'><div class='avatar'></div></div>"
                  }
                  else{
                      var innerHtml="<div class='conversation-part conversation-part--question'><div class='avatar-wrapper same-row'></div>"
                  }
              var object = arrayOfObjects[i];
              //console.log(object);

               if (('text' in object) && !('buttons' in object ) && (object['text'] != 'restarted')) {
                    innerHtml=innerHtml+"<div class='same-row question-part text-ltr'><div class='bubble no-border' style='display: table; direction: unset;'><div class='bubble-label'><div>"+object['text']+"</div></div></div>"+"<span class='comment' data-timestamp='"+moment().format("YYYY-MM-DD HH:mm:ss.SSS")+"'>just now</span>"+"</div>"
                }
                if ('image' in object) {
                    innerHtml=innerHtml+"<div class='same-row question-part text-ltr'><img src='"+object['image']+"' style='float:none;height: auto;width: auto'>"+"<span class='comment' data-timestamp='"+moment().format("YYYY-MM-DD HH:mm:ss.SSS")+"'>just now</span>"+"</div>"
                }
                if(('text' in object) && ('buttons' in object)){
                   innerHtml=innerHtml+"<div class='same-row question-part text-ltr'><div class='bubble no-border' style='display: table; direction: unset;'><div class='bubble-label'><div></div><div>"+object['text']+"</div>";
                   innerHtml=innerHtml+ "<div class='option-wrapper'>"
                   arrayOfBtns=object['buttons']
                   for (var j= 0; j < arrayOfBtns.length; j++) {
                    innerHtml=innerHtml+"<div class='bubble bubble-inline option theme-border theme-color' onclick='onButtonClick("+JSON.stringify(arrayOfBtns[j])+")' ><span class='option_n'></span><div class='option_title'>"+arrayOfBtns[j]['title']+"</div></div>";
                   }
                   innerHtml=innerHtml+"</div>"+"<span class='comment' data-timestamp='"+moment().format("YYYY-MM-DD HH:mm:ss.SSS")+"'>just now</span>"+"</div></div>"
                }
               innerHtml=innerHtml+"</div>"
                  //console.log("inner html for iteration"+ innerHtml);
               appendHTML=appendHTML+innerHtml

             }

             function explode(){
              $('.typing_loader').css("display", "none");
              $("#result_div").append(appendHTML);
              $('#result_div').animate({scrollTop: $('#result_div').get(0).scrollHeight},1000);

        }
        setTimeout(explode, 2000);
        $('#result_div').animate({scrollTop: $('#result_div').get(0).scrollHeight},1000);
	}


	socket.onopen = function(e) {
          console.log("[open] Connection established");
        };

    socket.onmessage = function(event) {
    var data = JSON.parse(event.data);

    if (data['type']=='bot_uttered'){
        appendBotMessage(data);
    }
    };

    socket.onclose = function(event) {

        console.log('[close] Connection died');
      };

    socket.onerror = function(error) {
         console.log("error");
    };


    $("#chat-input").keypress(function(e) {
            if (e.which === 13) {  // enter, return
                $('#send').click();
            }
        });

    $("#idReload").click(function() {
        var r=confirm("Do you want to restart this conversation?");
        if (r)
        {
            $("#result_div").html("");
            socket.send(JSON.stringify({
                "message":"I want to have restart conversation.",
                "type":"user_uttered"
                }))

           setTimeout(function(){
               socket.send(JSON.stringify({
                    "message":"hello",
                    "type":"user_uttered"
                    })) ;

                }, 100);

           $('#result_div').append(loaderHTMl);


        }

    })

	$("#send").click(function() {
		const chatInput = $("#chat-input").val();
		if (chatInput) {
			socket.send(JSON.stringify({
            "message":chatInput,
            "type":"user_uttered"
            }))

            html="<div class='conversation-part conversation-part--animation conversation-part--answer'><div class='answer text-ltr'><div class='bubble no-border theme-background'><div class='bubble-label-answer'>"+chatInput+"</div></div>"+"<span class='comment' data-timestamp='"+moment().format("YYYY-MM-DD HH:mm:ss.SSS")+"'>just now</span>"+"</span>"+"</div></div>"
			$("#result_div").append(html);
			$("#chat-input").val('')
			$('#result_div').animate({scrollTop: $('#result_div').get(0).scrollHeight});
			$('#result_div').append(loaderHTMl);
		}
	})

});


