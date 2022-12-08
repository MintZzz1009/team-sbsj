// 아이디 중복 확인
const userIdConfirm = document.querySelector('#user_id_confirm_button')
userIdConfirm.addEventListener('click', user_id_confirm)

// 동기 처리
function user_id_confirm() {
    console.log('# 아이디 확인 작업 시작')

    $('#user_id').removeClass('is-invalid is-valid');
    $('#id-feedback').remove()
    let user_id = $("#user_id").val();
    console.log('id: ', user_id)
    typeof (user_id)
    if ( user_id === '' ) {
        $('#user_id').addClass('is-invalid');
        $('#user_id_confirm_button').after(`<div id="id-feedback" class="invalid-feedback" style="text-align: right">아이디를 입력해주세요 😭</div>`)
        console.log('아이디 값이 없음')
        return
    }
    if ( user_id.includes(' ') === true || user_id.includes(',') === true ) {
        $('#user_id').addClass('is-invalid');
        $('#user_id_confirm_button').after(`<div id="id-feedback" class="invalid-feedback" style="text-align: right">아이디에 "공백"이나 ","가 포함되어서는 안됩니다 😭</div>`)
        console.log('아이디에 공백 및 쉼표 포함되어 실패')
        return
    }
    $.ajax({
        type: "POST",
        url: "/main/signup/userid",
        data: {
            user_id_give: user_id
        },
        async: false,
        success: function (response) {
            console.log('response[result]:', response["result"]);
            let result = response["result"];
            if (result === 'available') {
                $('#user_id').addClass('is-valid');
                $('#user_id_confirm_button').after(`<div id="id-feedback" class="valid-feedback" style="text-align: right">사용가능한 아이디입니다 😝</div>`)
                console.log('사용가능한 아이디')
            } else {
                $('#user_id').addClass('is-invalid');
                $('#user_id_confirm_button').after(`<div id="id-feedback" class="invalid-feedback" style="text-align: right">다른 아이디를 선택해주세요 😭</div>`)
                console.log('중복된 아이디')
            }
        },
    });
}



// 비밀번호 글자 수 확인
const pw = document.querySelector('#user_pw')
pw.addEventListener('focusout', user_pw_length_confirm)

function user_pw_length_confirm() {
    console.log('비밀번호 글자수 확인 작업 시작')
    $('#user_pw').removeClass('is-invalid is-valid');
    $('#pw-length-feedback').remove()
    let user_pw = $("#user_pw").val();
    console.log('1번째 칸 비밀번호: ', user_pw)
    console.log('비밀번호 글자 수: ', user_pw.length)

    if ( user_pw.includes(' ') == true || user_pw.includes(',') === true ) {
        $('#user_pw').addClass('is-invalid');
        $('#user_pw').after(`<div id="pw-length-feedback" class="invalid-feedback" style="text-align: right">비밀번호에 "공백"이나 ","가 포함되어서는 안됩니다 😭</div>`)
        console.log('비밀번호에 공백 및 쉼표 포함되어 실패')
        return false
    } else if (user_pw.length >= 4) {
        $('#user_pw').addClass('is-valid');
        $('#user_pw').after(`<div id="pw-length-feedback" class="valid-feedback" style="text-align: right">사용가능한 비밀번호입니다 😝</div>`)
        console.log('비밀번호 글자수 조건만족')
        return true
    } else {
        $('#user_pw').addClass('is-invalid');
        $('#user_pw').after(`<div id="pw-length-feedback" class="invalid-feedback" style="text-align: right">비밀번호의 글자수를 확인해주세요 😭</div>`)
        console.log('비밀번호 글자수 조건불만족')
        return false
    }

}


// 비밀번호랑 비밀번호 확인이랑 같은지 확인
const pwConfirm = document.querySelector('#user_pw_confirm')
pwConfirm.addEventListener('focusout', user_pw_confirm)

function user_pw_confirm() {
    console.log('비밀번호 확인 작업 시작')
    $('#user_pw_confirm').removeClass('is-invalid is-valid');
    $('#pw-feedback').remove()
    console.log('2번째 칸 비밀번호: ', pwConfirm.value)

    if (pw.value.length >= 4 && pw.value === pwConfirm.value) {
        $('#user_pw_confirm').addClass('is-valid');
        $('#user_pw_confirm').after(`<div id="pw-feedback" class="valid-feedback" style="text-align: right">비밀번호가 일치합니다 😝</div>`)
        console.log('비밀번호 일치')
        return true
    } else {
        $('#user_pw_confirm').addClass('is-invalid');
        $('#user_pw_confirm').after(`<div id="pw-feedback" class="invalid-feedback" style="text-align: right">비밀번호가 다릅니다 😭</div>`)
        console.log('비밀번호 불일치')
        return false
    }
}


// 이름 입력 확인
const name = document.querySelector('#user_name')
name.addEventListener('focusout', user_name_confirm)

function user_name_confirm() {
    console.log('이름 확인 작업 시작')
    $('#user_name').removeClass('is-invalid is-valid');
    $('#name-feedback').remove()
    console.log('이름 :', name.value)

    if (name.value.includes(' ') || name.value.includes(',') === true) {
        $('#name-feedback').addClass('is-invalid');
        $('#name-feedback').after(`<div id="name-feedback" class="invalid-feedback" style="text-align: right">이름에 "공백"이나 ","가 포함되어서는 안됩니다 😭</div>`)
        console.log('이름에 공백 및 쉼표 포함되어 실패')
        return false
    } else if (name.value.length >= 1) {
        $('#user_name').addClass('is-valid');
        $('#user_name').after(`<div id="name-feedback" class="valid-feedback" style="text-align: right">예쁜 이름이네요 😝</div>`)
        console.log('이름 확인 성공')
        return true
    } else {
        $('#user_name').addClass('is-invalid');
        $('#user_name').after(`<div id="name-feedback" class="invalid-feedback" style="text-align: right">다른 이름을 입력해주세요 😭</div>`)
        console.log('이름 확인 실패')
        return false
    }
}


// 이메일 입력 및 형식 확인
const email = document.querySelector('#user_email')
email.addEventListener('focusout', user_email_confirm)

function user_email_confirm() {
        console.log('이메일 확인 작업 시작')
        $('#user_email').removeClass('is-invalid is-valid');
        $('#email-feedback').remove()
        console.log('이메일 :', email.value)
        if (email.value.split('@').length === 2 && email.value.split('@')[1].split('.').length >= 2 && email.value.split('@')[1].split('.').length <= 3) {
            $('#user_email').addClass('is-valid');
            $('#user_email').after(`<div id="email-feedback" class="valid-feedback" style="text-align: right">멋진 이메일이군요 😝</div>`)
            console.log('이메일 확인 성공')
            // return true
        } else {
            $('#user_email').addClass('is-invalid');
            $('#user_email').after(`<div id="email-feedback" class="invalid-feedback" style="text-align: right">이메일 형식을 다시 확인해주세요 😭</div>`)
            console.log('이메일 확인 실패')
            // return false
        }
}


// 로그인시 form 확인 + post 요청
const signup = document.querySelector('#submit-signup')
signup.addEventListener('click', totalConfirm)

function totalConfirm() {
    user_id_confirm()
    user_pw_length_confirm()
    user_pw_confirm()
    user_name_confirm()
    user_email_confirm()

    console.log('아이디 확인 작업 시작')
    if (!$('#user_id').hasClass('is-valid')) {
        return alert('아이디가 올바른지 확인해주세요')
    }
    console.log('비밀번호 글자수 확인 작업 시작')
    if (!$('#user_pw').hasClass('is-valid')) {
        return alert('비밀번호의 글자 수가 올바른지 확인해주세요')
    }

    console.log('비밀번호 일치 확인 작업 시작')
    if (!$('#user_pw_confirm').hasClass('is-valid')) {
        return alert('비밀번호가 일치하는지 확인해주세요')
    }

    console.log('이름 확인 작업 시작')
    if (!$('#user_name').hasClass('is-valid')) {
        return alert('이름이 올바른지 확인해주세요')
    }

    console.log('이메일 확인 작업 시작')
    if (!$('#user_email').hasClass('is-valid')) {
        return alert('이메일이 올바른지 확인해주세요')
    }
    sign_up()
}

function sign_up() {

    let user_id = $("#user_id").val();
    let user_pw = $("#user_pw").val();
    let user_name = $("#user_name").val();
    let user_email = $("#user_email").val();
    console.log(user_id, user_pw, user_name, user_email)
    // let user_avatar = $("#user_avatar").val();
    // const user_avatar_img_file = new FormData();
    // user_avatar_img_file.append('user_avatar', $("#user_avatar")[0].files[0])
    // console.log(user_avatar_img_file)

    $.ajax({
        type: "POST",
        url: "/main/signup",
        data: {
            user_id_give: user_id,
            user_name_give: user_name,
            user_email_give: user_email,
            user_pw_give: user_pw,
            // user_avatar_img_file
            // user_pw_question_give : user_pw_question,
            // user_pw_answer_give : user_pw_answer
        },
        success: function (response) {
            console.log(response["doc"]);
            alert('회원가입 성공!')
            window.location.reload();
        },
    });
}
