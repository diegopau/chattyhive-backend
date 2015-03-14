/**
 * Created with PyCharm.
 * User: xurxo
 * Date: 24/01/14
 * Time: 4:27
 * To change this template use File | Settings | File Templates.
 */
var num_rep=0;
var user="{{ user }}";
var key="{{ key }}";
var channel_name="{{ channel }}";
var event_name="{{ event }}";
var chat="{{ chat_field }}";

// Connecting to pusher
var pusher = new Pusher(key);
var channel = pusher.subscribe(channel_name);

// Listening to the channel
channel.bind(event_name, function(data) {
    if(data.username!=user) write(data.username, data.message, data.timestamp, data.timestamp_server);
});

// AJAX method to write chat answers on screen
function write(name_user, text, timestamp, timestamp_server) {
    chat = $('#chat_field').html();
    num_rep ++;
    if (num_rep > 25) {
        $('#chat_field').text(name_user + " said: " + text + " &nbsp;&nbsp;&nbsp;&nbsp;  on: " + timestamp);
        $('#time').text("Last message on " + timestamp + " &nbsp;&mbsp;&nbsp;&nbsp;&nbsp; Received on server on " + timestamp_server);
        num_rep = 0;
    } else {
        $('#chat_field').html(chat + '<br/>' + name_user + " said: " + text + "&nbsp;&nbsp;&nbsp;&nbsp;   on: " + timestamp);
        $('#time').text("Last message: " + timestamp + "   Received on server on " + timestamp_server);
    }
}

// Buttons behaviour
$(document).ready(function() {
    // Button send behaviour when clicked
    $('#btn_send').on('click', function()
    {
        alert(channel_name);
        var text_sent = $("#msg_text").val();
        $("#msg_text").val("");
        var d = new Date();
        var timestamp = d.toTimeString();
        var timestamp_server = null;
        var csrftoken = $.cookie('csrftoken');
        $.ajax({
            type: "POST",
            url: "/test-ui/chat/" + channel_name + "/",
            headers: {"X-CSRFToken":csrftoken},
            data: {username:user, timestamp:timestamp, message:text_sent, timestamp_server:timestamp_server},
            success: function(newData){
                if(newData=="Server Ok") {
                    $("#status").html(newData);
                } else {
                    alert(newData);
                    location.href="/";
                }
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
        write(user, text_sent, timestamp, timestamp_server);
        return false;
    });

    // Button logout behaviour when clicked
    $('#btn_logout').on('click', function()
    {
        var csrftoken = $.cookie('csrftoken');
        $.ajax({
            type: "POST",
            url: "/test-ui/logout/",
            headers: {"X-CSRFToken":csrftoken},
            data: "",
            success: function(newData){
                alert(newData);
                //$.removeCookie(); TODO toggle to remove browser cookies
                location.href="/";
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
        return false;
    });
});