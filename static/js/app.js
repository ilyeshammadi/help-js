(function () {

    let objData = {};

    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {


        /**
         * Created by ilyes on 3/10/17.
         */
        // Note that the path doesn't matter right now; any WebSocket
        // connection gets bumped over to WebSocket consumers
        socket = new WebSocket("ws://" + window.location.host + "/chatroom/" + chatroomSessionID);

        const editor = ace.edit("editor");
        editor.setTheme("ace/theme/monokai");
        editor.getSession().setMode("ace/mode/python");
        editor.$blockScrolling = Infinity;
        document.getElementById('editor').style.fontSize = '15px';

        let id = Math.floor(Math.random() * 100);


        // connection
        socket.onopen = function () {
            // socket.send(JSON.stringify(objData));
        };

        // Receive the data here
        socket.onmessage = function (e) {
            let data = JSON.parse(e.data);
            if (data.id !== id) {
                editor.setValue(data.code);
                // console.log(data.msg);
                sendMessage(data.msg, 'left')
            }

        };


        $('#editor').keyup(function () {
            objData = {
                id: id,
                code: editor.getValue(),
                time: 12

            };

            socket.send(JSON.stringify(objData));
        });


        // Call onopen directly if socket is already open
        if (socket.readyState == WebSocket.OPEN) socket.onopen();


        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text, side) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message_side = side;
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({
                scrollTop: $messages.prop('scrollHeight')
            }, 300);
        };
        $('.send_message').click(function (e) {
            return sendMessage(getMessageText(), 'right');
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                //
                // objData.msg = getMessageText();
                // objData.id = id;
                // objData.code = editor.getValue();
                //

                objData = {
                    id: id,
                    msg: getMessageText(),
                    code: editor.getValue()

                };

                console.log(objData.code);

                socket.send(JSON.stringify(objData));
                return sendMessage(getMessageText(), 'right');
            }
        });


        // Timer
        var timer2 = "15:00";
        var interval = setInterval(function () {


            var timer = timer2.split(':');
            //by parsing integer, I avoid all extra string processing
            var minutes = parseInt(timer[0], 10);
            var seconds = parseInt(timer[1], 10);
            --seconds;
            minutes = (seconds < 0) ? --minutes : minutes;
            if (minutes < 0) clearInterval(interval);
            seconds = (seconds < 0) ? 59 : seconds;
            seconds = (seconds < 10) ? '0' + seconds : seconds;
            //minutes = (minutes < 10) ?  minutes : minutes;

            console.log(chatroomSessionID);


            // If time has ended
            if (minutes == 0 && seconds == 0) {
                // Session ended = true
                alert('Session time has ended');

                // Redirect
                window.location.replace('http://' + window.location.host + '/')
            }


            $('#countdown').html(minutes + ':' + seconds);
            timer2 = minutes + ':' + seconds;
        }, 1000);

        $('#myselect').change(function () {
            editor.getSession().setMode("ace/mode/" + $('#myselect :selected').val());
        })
    });


}.call(this));