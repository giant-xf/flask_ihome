function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$(function () {
    // 获取实名信息
    $.get('/api/v1.0/users/auth', function (resp) {
        // 用户未登录
        if (resp.errno=='4101'){
            location.href = '/login.html'
        }
        else if (resp.errno=='0'){
            // 如果返回的数据中real_name与id_card不为null，表示用户有填写实名信息
            if (resp.data.real_name&&resp.data.id_card){
                $("#real-name").val(resp.data.real_name)
                $("#id-card").val(resp.data.id_card)

                // 给input添加disabled属性，禁止用户修改
                $("#real-name").prop("disabled", true);
                $("#id-card").prop("disabled", true);
                // 隐藏提交保存按钮
                $("#form-auth>input[type=submit]").hide();
            }
        }else {
            alert(resp.errmsg)
        }
    })

    $('#form-auth').submit(function (e) {
        e.preventDefault()
        // 如果没有实名信息，展示错误信息
        realName = $("#real-name").val()
        idCard = $("#id-card").val()
        if (realName==''||idCard==''){
            $(".error-msg").show()
        }
        data={
            real_name : realName,
            id_card : idCard
        }
        jsonData = JSON.stringify(data)

        $.ajax({
            url: '/api/v1.0/users/auth',
            type:'post',
            data:jsonData,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFTOKEN": getCookie("csrf_token")
            },
            success: function (resp) {
                if (0 == resp.errno) {
                    $(".error-msg").hide();
                    // 显示保存成功的提示信息
                    showSuccessMsg();
                    $("#real-name").prop("disabled", true);
                    $("#id-card").prop("disabled", true);
                    $("#form-auth>input[type=submit]").hide();
                }
            }

        })



    })

})





