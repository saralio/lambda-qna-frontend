const options = [...document.getElementsByName('option')]
const submit = document.getElementById('submit')

function anySelected() {
    return options.some(x => x.checked)
}

options.forEach(option => {
    option.addEventListener('click', () => {
        anySelected() ? submit.removeAttribute('disabled') : submit.setAttribute('disabled', '')
    })
})

anySelected() ? submit.removeAttribute('disabled') : submit.setAttribute('disabled', '')

corrAnsLabel = document.getElementById('correct-ans-text-label')
incorrAnsLabel = document.getElementById('incorrect-ans-text-label')
answer = document.getElementsByClassName('answer-text')[0]
links = document.getElementsByClassName('links')[0]

function checkAnswer() {
    if (anySelected()) {
        options.forEach(option => {
            if (option.checked) {
                if (option.getAttribute('correct-answer') == 'True') {
                    corrAnsLabel.style.display = "block";
                    submit.style.display = "none";
                } else {
                    incorrAnsLabel.style.display = "block";
                    submit.style.display = "none"
                }
            }
        })
    }
    answer.style.visibility = "visible";
    links.style.visibility = "visible";
}