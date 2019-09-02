function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击推出按钮时执行的函数
function logout() {
    $.ajax({
        url: "/api/v1.0/logout",
        type: "delete",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if (resp.errno == "0") {
                location.href = "/index.html";
            }
        }
    });
}

$(document).ready(function(){

    // 获取用户名和手机号
    $.get('/api/v1.0/users', function (resp) {
        // 用户未登录
        if (resp.errno=='4101'){
            location.href = '/login.html'
        }
        else if (resp.errno == '0'){
            if(resp.data.avatar){
                $("#user-avatar").attr('src', resp.data.avatar)
            }
            $("#user-name").html(resp.data.name)
            $("#user-mobile").html(resp.data.mobile)
        }else {
            alert(resp.errmsg)
        }

    })

})