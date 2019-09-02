function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    // 修改头像
    $("#form-avatar").submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url: '/api/v1.0/users/avatar',
            type: 'post',
            // data默认帮我们处理了
            dataType: 'json',
            headers: {
              'X-CSRFToken': getCookie('csrf_token')
            },
            success:function (resp) {
                if (resp.errno == '0'){
                    // 上传成功
                    avatarUrl = resp.data.avatar_url;
                    $('#user-avatar').attr('src',avatarUrl);
                }else {
                    alert(resp.errmsg);
                }
            }
        })
    })

    // 获取用户的头像和用户名
    $.get('/api/v1.0/users',function (resp) {
        if (resp.errno =='4001'){
            location.href = '/login.html'
        }
        else if (resp.errno=='0'){
            $('#user-name').val(resp.data.name)
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    });

    // 修改用户名
    $("#form-name").submit(function (e) {
        e.preventDefault();
        name = $('#user-name').val()
        if (!name) {
            alert("请填写用户名！");
            return;
        }

        $.ajax({
            url: '/api/v1.0/users/name',
            type: 'PUT',
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: 'json',
            headers: {
              'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0') {
                    $('.error-msg').hide()
                    showSuccessMsg()
                }
                else if (resp.errno == "4001") {
                    $(".error-msg").show();
                }
                else if("4101" == resp.errno) {
                    location.href = "/login.html";
                }else {
                    alert(errmsg)
                }
            }
        });
    })

});