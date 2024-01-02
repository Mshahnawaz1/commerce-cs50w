// this is for following btn  toggle
document.addEventListener('DOMContentLoaded', function () {

  const btn = document.querySelector('#follow-btn')

  btn.addEventListener('click', () => {
    console.log("clicked...")
    const user = btn.dataset.user
    const action = btn.textContent.trim()
    
    console.log(user + action)

    form = new FormData();
    form.append("user", user);
    form.append("action", action);

    fetch('/follow/', {
      method: 'POST',
      body: form
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data)
        if(data.status == 201){
          btn.textContent = data.action
          document.querySelector('#followers').innerHTML = `Followers: ${data.followers}`
        }

      })
  })
});