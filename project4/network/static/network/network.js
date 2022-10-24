edit = document.querySelectorAll(".edit");
text_area = document.querySelectorAll(".textarea");

document.querySelectorAll('.fa-heart').forEach(div => {
  div.onclick = function () {
      likeDislike(this);
  };
});

edit.forEach((element) => {
    element.addEventListener("click", () => {
      edit_handeler(element);
    });
  });
  
  text_area.forEach((element) => {
    element.addEventListener("keyup", (e) => {
      if (e.keyCode == 13 && e.shiftKey) return;
      if (e.keyCode === 13) edit_handeler(element);
    });
  });
  
  function editpost(id, post) {
    form = new FormData();
    form.append("id", id);
    form.append("post", post.trim());
  
    fetch("/editpost/", {
      method: "POST",
      body: form,
    }).then((res) => {
      document.querySelector(`#post-content-${id}`).textContent = post;
      document.querySelector(`#post-content-${id}`).style.display = "block";
      document.querySelector(`#edit-post-${id}`).style.display = "none";
      document.querySelector(`#edit-post-${id}`).value = post.trim();
    });
  }
  
  function edit_handeler(element) {
    id = element.getAttribute("data-id");
    edit_btn = document.querySelector(`#edit-btn-${id}`);
    if (edit_btn.textContent == "Edit") {
      document.querySelector(`#post-content-${id}`).style.display = "none";
      document.querySelector(`#edit-post-${id}`).style.display = "block";
      edit_btn.textContent = "Save";
    } else if (edit_btn.textContent == "Save") {
      editpost(id, document.querySelector(`#edit-post-${id}`).value);
  
      edit_btn.textContent = "Edit";
    }
  }

  async function likeDislike(element) {
    await fetch(`/likeDislike/${element.dataset.id}`)
        .then(response => response.json())
        .then(data => {
            element.className = data.css;
            element.querySelector('small').innerHTML = data.likes;
        });
}