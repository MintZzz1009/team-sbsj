document.addEventListener('DOMContentLoaded', () => {

    const goHome = document.querySelector('#go-home')
    goHome.addEventListener('click', handleGoHome)

    function handleGoHome () {
        window.location.href='/'
    }
})