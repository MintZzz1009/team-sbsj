document.addEventListener('DOMContentLoaded', () => {

    const goMyPage = document.querySelector('#go-mypage')
    goMyPage.addEventListener('click', handleGoMyPage)

    function handleGoMyPage () {
        window.location.href='/mypage'
    }
})