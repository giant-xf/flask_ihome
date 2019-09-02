function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

    error_mobile = false;
    error_password = false;

    $('#mobile').blur(function () {
        check_mobile()
    });
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });

    $("#password").blur(function () {
        check_password()
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });

    // 校验手机号
    function check_mobile() {
        // 判断手机号正确性
        mobile = $("#mobile").val();
        re = /^1[35678]\d{9}$/;
        if(re.test(mobile)){
            $('#mobile-err').hide();
            error_mobile = false;
        }else {
            $('#mobile-err span').html('您输入的手机号码格式不正确！');
            $('#mobile-err').show();
            error_mobile = true;
        }
    }
    // 校验密码格式
    function check_password() {
        passwd = $("#password").val();
        var len = passwd.length;
        if(len<6||len>20)
        {
            $('#password-err span').html('密码最少6位，最长20位')
            $('#password-err').show();
            error_password = true;
        }
        else
        {
            $('#password-err').hide();
            error_password = false;
        }
    }


    $(".form-login").submit(function(e){
        e.preventDefault();
        // mobile = $("#mobile").val();
        // passwd = $("#password").val();
        // if (!mobile) {
        //     $("#mobile-err span").html("请填写正确的手机号！");
        //     $("#mobile-err").show();
        //     return;
        // }
        // if (!passwd) {
        //     $("#password-err span").html("请填写密码!");
        //     $("#password-err").show();
        //     return;
        // }

        check_mobile();
        check_password();
        if (error_mobile==false && error_password==false) {
            // 调用ajax向后端发送注册请求
            data = {
                mobile: mobile,
                password: passwd
            };
            // 转换成json格式
            data = JSON.stringify(data);
            $.ajax({
                url: '/api/v1.0/login',
                type: 'post',
                data: data,
                contentType: 'application/json',
                dataType: 'json',
                // 添加响应头，获取csrf_token，相当于在body中设置csrf_token
                headers: {
                    "X-CSRFToken": getCookie('csrf_token')
                },
                success: function (res) {
                    if (res.errno == '0') {
                        // 登录成功,跳转到主页
                        location.href = '/index.html'
                    } else {
                        alert(res.errmsg)
                    }
                }
            })

        }else {return false}


    });
})