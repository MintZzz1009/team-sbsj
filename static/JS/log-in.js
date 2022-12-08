// 아이디 중복 확인
const LogIn = document.querySelector('#submit-login')
LogIn.addEventListener('click', submit_log_in)

// 동기 처리
function submit_log_in() {
    console.log('로그인 시도!')
    let input_id = $('#inputId').val()
    console.log(input_id)
    let input_pw = $('#inputPassword').val()
    console.log(input_pw)
    $.ajax({
        type: "POST",
        url: "/main/login",
        data: {
            input_id_give: input_id,
            input_pw_give: input_pw
        },
        async: false,
        success: function (response) {
            console.log(response);
            let result = response["msg"];
            if (result === 'fail') {
                alert('아이디를 찾을 수 없습니다')
                console.log('아이디 확인 실패')
            } else if (result === 'wrong_pw') {
                alert('비밀번호가 틀립니다')
                console.log('비밀번호 확인 실패')
            } else {
                // 로그인
                console.log('로그인 성공!')
                alert('로그인 성공!')
                window.location.reload();
            }
        },
    });
}