/**
 * Created with PyCharm.
 * User: xurxo
 * Date: 6/11/13
 * Time: 0:06
 * To change this template use File | Settings | File Templates.
 */

        // TODO that's for creating our own form, not used yet
        function send_post(msg_text) {
            var form = document.createElement("FORM");
            form.method = 'POST';
            form.action = '/test-ui/chat/';
            form.value = msg_text;
            alert(msg_text);
            form.submit();
        }

        function send_jquery(msg_text){
//            var sortid = $('#sort').val().toLowerCase();
//            alert("send_jquery")
            $.ajax({
//                alert("ajax1");
//                print('ajax1');
                type:"POST",
                url: "/test-ui/chat/",
                data: {msg: msg_text},
                success: function(newData){
                    document.getElementById("chat_field").html('---->ok');
                    write('test', '------>ok');
                }
            });
            alert("jquery working");
        }

        /*
        // Gets the cookie or creates a new one if it doesn't exist
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
        */

        // Deletes all the content of the cookie and sets expire-date already expired
        function deleteAllCookies() {
            //$.removeCookie();
            /*
            var cookies = document.cookie.split(";");
//            alert(cookies.length);
            for (var i = 0; i < cookies.length; i++) {
    	        var cookie = cookies[i];
//                alert(cookie);
    	        var eqPos = cookie.indexOf("=");
    	        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    	        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
            }
            */
            //alert("bu");
        }

        /*
        // Loads part of the webpage - AJAX
        function loadXMLDoc(text_sent) {

            var csrftoken = $.cookie('csrftoken');
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
//            xmlhttp.setRequestHeader("user",user);
//            xmlhttp.setRequestHeader("msg",text_sent);
//            xmlhttp.send("user="+user+"&msg="+text_sent);
            xmlhttp.send('{"user":"'+user+'","msg":"'+text_sent+'"}');
//            xmlhttp.ajaxSend() fixme
        }
        */

        /*
        // Button Send behaviour
        function onClick() {
            //var text_sent = $("#msg_text").val();
            //$("#msg_text").val("");
            //write(user, text_sent);
            //loadXMLDoc(text_sent);
        }
        */

                // Deletes all the content of the cookie and sets expire-date already expired
        function deleteAllCookies_jQuery() {
            $.removeCookie();
        }

        /*
        // Button Logout behaviour
        function onLogout() {
            // TODO cookies deleted locally, still should send some POST for the server to update
            var csrftoken = $.cookie('csrftoken');
            var xmlhttp;
            if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
                xmlhttp=new XMLHttpRequest();
            }
            else {// code for IE6, IE5
                xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
            }
            xmlhttp.open("POST","/logout/",true);
            xmlhttp.setRequestHeader("X-CSRFToken",csrftoken);
            xmlhttp.send('');
            deleteAllCookies_jQuery();
            location.href="/";
        }*/

        $(document).ready(function() {
            $('send_msg').submit(function()
            {
                alert("submit_catched")
                $.ajax({
                    type: "POST",
                    url: "/test-ui/chat/",
                    data: {msg: msg_text},
                    success: function(newData){
                        document.getElementById("chat_field").html('---->ok');
                    },
                    failure: function(errMsg) {
                        alert(errMsg);
                    }
                });
                return false;
            });
        });