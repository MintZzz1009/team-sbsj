



document.addEventListener('DOMContentLoaded', () => {


    const button = document.querySelector('#button')
    button.addEventListener('click', addclock)

    function addclock() {
        const clock = document.querySelector('#clock')
        const div = document.querySelector('#div')
        div.append("20:35")
        clock.append("09:23")
    }

})




