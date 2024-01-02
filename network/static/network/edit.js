
document.addEventListener('DOMContentLoaded', function () {

    document.addEventListener('click', function (event) {
        // here should check if div is clicked instead of btn
        const btn = event.target;
        console.log(btn.id)
        if (btn.id == "edit-btn") {
            const id = btn.dataset.id;
            const action = btn.dataset.action;
            const user = btn.dataset.user;
            const parentElement = document.querySelector(`#post-${id}`)


            console.log(btn.dataset.id, btn.dataset.action, btn.dataset.user)
            if (btn.dataset.action == "edit") {
                // when btn clicked for edit
                const postText = document.querySelector(`#post-text-${id}`);

                // create a new textarea
                const textArea = document.createElement('textarea')
                textArea.id = `text-area-${id}`
                textArea.value = postText.textContent.replace("Post: ", "");
                textArea.rows = 3;
                textArea.cols = 60;

                parentElement.replaceChild(textArea, postText)

                btn.dataset.action = "submit";
                btn.innerHTML = "Submit";

            }
            else if (btn.dataset.action == "submit") {
                const post = document.querySelector(`#text-area-${id}`).value
                console.log(post)

                form = new FormData()
                form.append("id", id)
                form.append("post", post)

                fetch("edit/", {
                    method: "POST",
                    body: form,
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    }
                })

                    .then(response => {
                        if (!response.ok) {
                            console.log()
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(res => {
                        console.log(res.post)
                        const textArea = document.querySelector(`text-area-${id}`)

                        const postElement = document.createElement('p')
                        postElement.id = `post-text-${id}`
                        postElement.textContent = res.post

                        parentElement.replaceChild(postElement, textArea)
                        btn.dataset.action = "submit";
                        btn.innerHTML = "Submit";
                    })
            }

        }
    })
})

// Copied from django documentation
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}