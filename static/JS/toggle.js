
// 토픽 토글 스위치
document.addEventListener('DOMContentLoaded', () => {
    console.log(document.querySelector('#topics__title'))

    const topicsTitle = document.querySelector('#topics__title')
    topicsTitle.addEventListener('click', toggleTopics1)

    function toggleTopics1() {
        const toggle = document.querySelector('#toggle-topics')
        toggle.style.transform = "rotate(90deg)"

        const categories = document.querySelector('#topics__categories')
        categories.style.visibility = 'visible'
        categories.style.opacity = '1'

        const topicsTitle = document.querySelector('#topics__title')
        topicsTitle.addEventListener('click', toggleTopics2)
        topicsTitle.removeEventListener("click", toggleTopics1)
    }

    function toggleTopics2() {
        const toggle = document.querySelector('#toggle-topics')
        toggle.style.transform = "rotate(0deg)"

        const categories = document.querySelector('#topics__categories')
        categories.style.visibility = 'hidden'
        categories.style.opacity = '0'


        const topicsTitle = document.querySelector('#topics__title')
        topicsTitle.addEventListener('click', toggleTopics1)
        topicsTitle.removeEventListener("click", toggleTopics2)
    }
});


