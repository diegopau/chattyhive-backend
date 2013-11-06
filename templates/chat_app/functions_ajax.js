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
            form.action = '/chat/';
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
                url: "/chat/",
                data: {msg: msg_text},
                success: function(newData){
                    document.getElementById("chat_field").html('---->ok');
                    write('test', '------>ok');
                }
            });
            alert("jquery working");
        }