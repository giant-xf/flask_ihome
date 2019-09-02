
// 获取cookie信息的函数
function getCookie(name) {
    // 正则表达式匹配'\b'表示边界，[^;]表示出了';'结尾
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 保存图片验证码编号
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 生成图片验证码的后端地址，设置到页面中，让浏览器请求验证码图片
    // 生成图片验证码编号
    imageCodeId = generateUUID();
    // 是指图片url
    url = '/api/v1.0/image_codes/'+imageCodeId;
    $('.image-code img').attr('src',url);

}

// 发送短信验证码函数
function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    data = {
        image_code:imageCode,
        image_code_id:imageCodeId
    };
    $.get('/api/v1.0/sms_codes/' + mobile, data, function (res) {
        // res 是后端返回的响应值，因为后端返回的是json字符串，
        // 所以ajax帮我们把这个json字符串转换成了json对象，res就是转换后的对象
        if (res.errno == '0') {
            // 表示发送成功
            num = 60;

            // 修改倒计时文本
            timer = setInterval(function () {
                if (num > 1) {
                    $('.phonecode-a').html(num + 's');
                    num -= 1;
                }
                else {
                    // 加上点击事件，修改文本
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    $('.phonecode-a').html('获取验证码');
                    clearInterval(timer)
                }
            }, 1000, 60)
        }
        else {
            // 其他错误的话直接弹出来提示
            alert(res.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }

    });
}



// 加载全局页面
$(document).ready(function() {
    generateImageCode();
    // $("#mobile").focus(function(){
    //     $("#mobile-err").hide();
    // });
    // $("#imagecode").focus(function(){
    //     $("#image-code-err").hide();
    // });
    // $("#phonecode").focus(function(){
    //     $("#phone-code-err").hide();
    // });
    // $("#password").focus(function(){
    //     $("#password-err").hide();
    //     $("#password2-err").hide();
    // });
    // $("#password2").focus(function(){
    //     $("#password2-err").hide();
    // });


    error_mobile = false;
    error_phoneCode = false;
    error_password = false;
    error_password2 = false;

    $('#mobile').blur(function () {
        check_mobile()
    });
    $('#mobile').focus(function () {
        $('#mobile-err').hide();
    });

    $("#phonecode").blur(function () {
        check_phoneCode()
    });
    $("#phonecode").focus(function () {
        $('#phone-code-err').hide();
    });

    $("#password").blur(function () {
        check_password()
    });
    $("#password").focus(function () {
       $('#password-err').hide();
    });

    $("#password2").blur(function () {
        check_password2()
    });
    $("#password2").focus(function () {
        $('#password2-err').hide();
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
            $('#mobile-err span').html('您输入的手机号码不存在！');
            $('#mobile-err').show();
            error_mobile = true;
        }
    }
    // 校验验证码是否输入
    function check_phoneCode() {
        phoneCode = $("#phonecode").val();
        if (phoneCode){
            $('#phone-code-err').hide();
            error_phoneCode = false
        }else {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            error_phoneCode = true
        }
    }
    // 校验密码格式
    function check_password() {
        passwd = $("#password").val();
        var len = passwd.length;
        if(len<8||len>20)
        {
            $('#password-err span').html('密码最少8位，最长20位')
            $('#password-err').show();
            error_password = true;
        }
        else
        {
            $('#password-err').hide();
            error_password = false;
        }
    }
    // 确认密码校验
    function check_password2() {
        passwd2 = $("#password2").val();
        if(passwd != passwd2)
        {
            $('#password2-err span').html('两次输入的密码不一致')
            $('#password2-err').show();
            error_password2 = true;
        }
        else
        {
            $('#password2-err').hide();
            error_password2 = false;
        }
    }




    // 在页面加载完成时，就拦截表单
    // 为表单提交补充自定义的函数行为  [提交事件(e)]
    $(".form-register").submit(function(e){
        // 在页面加载完成时，就拦截表单
        e.preventDefault();

        // mobile = $("#mobile").val();
        // phoneCode = $("#phonecode").val();
        // passwd = $("#password").val();
        // passwd2 = $("#password2").val();
        // if (!mobile) {
        //     $("#mobile-err span").html("请填写正确的手机号！");
        //     $("#mobile-err").show();
        //     return;
        // }
        // if (!phoneCode) {
        //     $("#phone-code-err span").html("请填写短信验证码！");
        //     $("#phone-code-err").show();
        //     return;
        // }
        // if (!passwd) {
        //     $("#password-err span").html("请填写密码!");
        //     $("#password-err").show();
        //     return;
        // }
        // if (passwd != passwd2) {
        //     $("#password2-err span").html("两次密码不一致!");
        //     $("#password2-err").show();
        //     return;
        // }
        check_mobile();
        check_phoneCode();
        check_password();
        check_password2();
        if (error_mobile==false &&error_phoneCode==false && error_password==false && error_password2==false) {
            // 调用ajax向后端发送注册请求
            data = {
                mobile: mobile,
                sms_code: phoneCode,
                password: passwd,
                password2: passwd2
            };
            // 转换成json格式
            data = JSON.stringify(data);
            $.ajax({
                url: '/api/v1.0/users',
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
                        // 注册成功,跳转到主页
                        location.href = '/index.html'
                    } else {
                        alert(res.errmsg)
                    }
                }
            })
        }else {
            return false
        }

    });
})