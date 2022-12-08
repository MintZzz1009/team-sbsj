const logOut = document.querySelector('#log-out')
logOut.addEventListener('click', log_out)

function log_out() {


    $.ajax({
        type: "GET",
        url: "/main/logout",
        data: {},
        success: function (response) {
            console.log(response['msg'])
            alert('로그아웃!')
            window.location.reload();


            }
        })

}