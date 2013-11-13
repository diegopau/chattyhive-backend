/**
 * Created with PyCharm.
 * User: xurxo
 * Date: 8/11/13
 * Time: 16:55
 * To change this template use File | Settings | File Templates.
 */

    src = '';


    var num_rep = 0;
    var user = $.parseJSON('{{ user }}');
    var app_key = $.parseJSON('{{ app_key }}');
    var key = $.parseJSON('{{ key }}');
    var channel_name = $.parseJSON('{{ channel }}');
    var event_name = $.parseJSON('{{ event }}');
    var chat = $.parseJSON('{{ chat_field }}');

    // Connecting to pusher
    var pusher = new Pusher(key);
    var channel = pusher.subscribe(channel_name);

    // Listening to the channel
    channel.bind(event_name, function(data) {
        if(data.user!=user) write(data.user,data.msg);
    });



    // AJAX method to write chat answers on screen
    function write_jquery(name_user, text) {
        num_rep ++;
        if (num_rep > 25) {
//            document.getElementById("chat_field").innerHTML ="<br/>" + name_user + " said: " + text;
            $('#chat_field').addText("<br/>" + name_user + " said: " + text);
            num_rep = 0;
        } else {
//            document.getElementById("chat_field").innerHTML +="<br/>" + name_user + " said: " + text;
            $('#chat_field').text("<br/>" + name_user + " said: " + text);
        }
    }

    // AJAX method to write chat answers on screen
    function write(name_user, text) {
        chat = document.getElementById("chat_field").valueOf(); // TODO trying to store previous messages
//        alert(chat);
        num_rep ++;
        if (num_rep > 25) {
            document.getElementById("chat_field").innerHTML ="<br/>" + name_user + " said: " + text;
            num_rep = 0;
        } else {
            document.getElementById("chat_field").innerHTML +="<br/>" + name_user + " said: " + text;
        }
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function loadXMLDoc(text_sent) {
//            returns 403: forbidden request, think because of the crsf missed

        var csrftoken = getCookie('csrftoken');
//        var csrftoken = $.cookie('csrftoken');
        var xmlhttp;
        if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
        }
        else {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                document.getElementById("chat_field").innerHTML+=xmlhttp.responseText;
            }
        }
        xmlhttp.open("POST","/chat/",true);
        xmlhttp.setRequestHeader("X-CSRFToken",csrftoken);
//        xmlhttp.setRequestHeader("user",user);
//        xmlhttp.setRequestHeader("msg",text_sent);
        xmlhttp.send("user="+user+"&msg="+text_sent);
//        xmlhttp.ajaxSend() fixme
    }


    $(document).ready(function(){
        alert("Hello");
        $('btn_send').on('click', function() {
            var input = $('#msg_text');
            var text_sent = input.text();
            input.html("");
            write(user, text_sent);
            /*$.ajax({
                type: "POST",
                url: "/chat/",
                data: "{user:"+user+";msg:"+text_sent+"}",
                success: "True"
//                dataType: dataType
            });*/
            loadXMLDoc(text_sent);
        })
    })