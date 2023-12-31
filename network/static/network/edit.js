

document.addEventListener("DOMContentLoaded", function () {

    const edits = document.querySelectorAll('.edit');

    edits.forEach((edit, index) => {
        edit.addEventListener('click', () => {

            let post = document.querySelectorAll('.post-text')[index]
            document.querySelectorAll('.form-edit')[index].style.display = "block";
            post.style.display = "none"
            edit.style.display = "none";

            // gets id of post
            const id = edit.dataset.id
            const user = edit.dataset.user
            const post_text = post.textContent.replace("Post: ", "")
            console.log(id, user)

            form = new FormData()
            form.append("user", user)
            form.append("post", post_text)
            form.append("id", id)

            // here id could be sent via get or post 
            fetch("edit/",{
                method: "POST",
                body : form
            })

            .then(res => {
                if(!res.ok){
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(res => {
                console.log(res)
            })
            

            
        });
    });

})








// document.addEventListener("DOMContentLoaded", function () {

//     // document.addEventListener('click', event => {

//     //     const element=event.target;
//     //     if (element.className= "edit")
//     //     {
//     //         document.querySelector('.', '.form-edit').style.display = "block";
//     //         element.style.display = "none";
//     //         post = document.querySelector('.post-text');
//     //     }
//     // })
//     let edits = document.querySelectorAll('.edit')
//     edits.forEach((edit, index) => {
//         edit.addEventListener('click',() => {

//             document.querySelector('form-edit').style.display = "block"
//             edit.style.display = 'none';
//             document.querySelectorAll('post-text').style.display = "none";
//             console.log("editing.......")
//         })
// })

// })

