let currentInterval;

document.addEventListener('DOMContentLoaded', () => {

    if (window.location.pathname === '/') {
        loadPosts(1, 'all');
        document.getElementById('all-posts').classList.add('active');

        if (document.getElementById('username')) {
            document.getElementById('username').classList.remove('active');
            document.getElementById('following').classList.remove('active');

            document.getElementById('publish').addEventListener('click', (event) => { savePost(document.getElementById('new-post'), 'new', 1, event, 'all'); });

        } else {
            document.getElementById('scroll').classList.remove('col-md-8');
            document.getElementById("login").classList.remove("active");
            document.getElementById("register").classList.remove("active");
        }

    } else if (/following/.test(window.location.pathname)) {
        document.getElementById('all-posts').classList.remove('active');
        document.getElementById('username').classList.remove('active');
        document.getElementById('following').classList.add('active');
        
        loadPosts(1, 'following');

    } else if (/profile/.test(window.location.pathname)) {
        document.getElementById('username').classList.add('active');
        document.getElementById('all-posts').classList.remove('active');
        document.getElementById('following').classList.remove('active');

        loadPosts(1, 'profile');
        online_users();
        setInterval(() => { online_users(); }, 60000);

    } else if (/login/.test(window.location.pathname)) {
        document.getElementById('login').classList.add('active');
        document.getElementById('register').classList.remove('active');
        document.getElementById('all-posts').classList.remove('active');

    } else if (/register/.test(window.location.pathname)) {
        document.getElementById('register').classList.add('active');
        document.getElementById('login').classList.remove('active');
        document.getElementById('all-posts').classList.remove('active');
    }
});


function savePost(form, action, page, event, amount, postId = 'new') {
    event.preventDefault();
    form.classList.add('was-validated');
    if (form.checkValidity()) {
        fetch(`/save_post/${action}`, {
        method: 'POST',
        body: JSON.stringify({
            content: document.getElementById(`${postId}`).value,
            post_id: postId,
        }),
        })
        .then((response) => {
            if (response.status === 201) {
                form.classList.remove('was-validated');
                document.getElementById(`${postId}`).value = '';
                loadPosts(page, amount);
            } else {
            return response.json().then((data) => {
                throw new Error(data.error);
            });
            }
        })
        .catch((error) => {
            const alert = document.createElement('span');
            alert.className = 'alert';
            alert.innerText = error.message;
            form.appendChild(alert);
            setTimeout(() => {
            alert.remove();
            }, 10000);
        });
    } else {
        event.stopPropagation();
    }
}


function loadPosts(page, action) {

    const paginator = document.getElementById('paginator')
    const postList = document.querySelector('#posts')
    postList.innerHTML = '';
    paginator.innerHTML = '';
    
    fetch(`/load_posts/${page}`, {
        method: 'POST',
        body: JSON.stringify({
            action: action}),
        })
        .then((response) => response.json())
        .then((data) => {
            for (let post of data.posts) {
                const postDiv = document.createElement('div');
                postDiv.classList.add('container', 'mb-3');

                const author = document.createElement('h5');
                author.innerHTML = `${post.author}`;
                postDiv.appendChild(author);

                const timestamp = document.createElement('p');
                timestamp.classList.add('timestamp');
                timestamp.innerHTML = `${post.timestamp}`;
                postDiv.appendChild(timestamp);

                const subject = document.createElement('div');
                subject.classList.add('subject');
                subject.id = `body-${post.id}`;
                subject.innerHTML = `${post.body}`;
                postDiv.appendChild(subject);

                const likeButton = document.createElement('button');
                likeButton.id = `like-${post.id}`;
                likeButton.innerHTML = `&#128077 ${post.likes_count}`;
                likeButton.classList.add('btn', 'btn-outline-success', 'btn-sm', 'me-2');
                if (post.likes.includes(data.current_user)) {
                    likeButton.classList.add('active')
                }
                likeButton.addEventListener('click', () => likePost(post, data.page_number, action));
                postDiv.appendChild(likeButton);

                if (data.current_user === post.author) {
                    const edit = document.createElement('button');
                    edit.classList.add('btn', 'btn-outline-secondary', 'btn-sm')
                    edit.id = `edit-${post.id}`;
                    edit.innerHTML = 'Edit';
                    edit.addEventListener('click', () => editPost(post, data.page_number, action));
                    postDiv.appendChild(edit);
                }

                const line = document.createElement('hr')
                postDiv.appendChild(line)

                postList.appendChild(postDiv);
            }
            if (data.page_number > 1) {
                const previous = document.createElement('li');
                previous.classList.add('page-item');
                previous.innerHTML = `<button class='page-link' onclick='loadPosts(${data.page_number - 1}, "${action}")'>Previous</button>`;
                paginator.appendChild(previous);
            }
            if (data.page_number < data.pages) {
                const next = document.createElement('li');
                next.classList.add('page-item');
                next.innerHTML = `<button class='page-link' onclick='loadPosts(${data.page_number + 1}, "${action}")'>Next</button>`;
                paginator.appendChild(next);
            }
            if (currentInterval) {
                clearInterval(currentInterval);
            }
            currentInterval = setInterval(() => { loadPosts(data.page_number, action); }, 60000);
        })
        .catch((error) => {
            console.log(error);
        });
}


function editPost(post, page_number, amount) {
    if (currentInterval) {
        clearInterval(currentInterval);
    }
    
    const edit = document.getElementById(`edit-${post.id}`);
    const body = document.getElementById(`body-${post.id}`);
    const editForm = document.createElement('form');

    editForm.setAttribute('novalidate', 'true');
    edit.style.display = 'none';
    editForm.innerHTML = `<textarea class='form-control' id='text-${post.id}' name='body' rows='5' spellcheck='on' maxlength='25000' required>${body.innerHTML}</textarea>
                    <button type='submit' id='save' class='btn btn-primary mt-2 btn-sm'>Save</button>`;

    body.replaceChild(editForm, body.firstChild);
    document.getElementById(`text-${post.id}`).focus();
    document.getElementById('save').addEventListener('click', (event) => { savePost(editForm, 'edit', page_number, event, amount, `text-${post.id}`); })
}


function online_users() {
    const usersList = document.querySelector('#scroll');
    usersList.innerHTML = '<h3>Online Users</h3>';

    fetch('/online_users')
        .then((response) => response.json())
        .then((data) => {
        for (let user of data.users_info) {
            const userDiv = document.createElement('div');
            userDiv.classList.add('container', 'mt-3');

            const username = document.createElement('h5');
            username.innerHTML = `${user.username}`;
            userDiv.appendChild(username);

            const follow = document.createElement('button');
            if (user.follower) {
                follow.innerHTML = 'Unfollow';
                follow.classList.add('btn', 'btn-outline-danger', 'btn-sm');
            } else {
                follow.innerHTML = 'Follow';
                follow.classList.add("btn", "btn-outline-success", "btn-sm");
            }
            follow.addEventListener('click', () => { followUser(user.follower, user.username) });
            userDiv.appendChild(follow);

            usersList.appendChild(userDiv);
        }
        document.getElementById('followers').innerHTML = `Followers: ${data.followers}`;
        document.getElementById('following-users').innerHTML = `Following: ${data.following}`;
        })
        .catch((error) => {
        console.log(error);
        });
}

function followUser(follower, username) {
    fetch('/follow', {
      method: 'POST',
      body: JSON.stringify({
        follower: follower,
        username: username,
      }),
    })
        .then((response) => {
                if (response.status != 200) {
                    return response.json().then((data) => {
                        throw new Error(data.error);
                    });
                }
            })
        .then(() => { online_users(); })
        .catch((error) => {
            console.log(error);
        });
}


function likePost(post, page, action) {
    fetch(`/like/${post.id}`)
      .then((response) => {
        if (response.status != 200) {
          return response.json().then((data) => {
            throw new Error(data.error);
          });
        }
      })
      .then(() => { loadPosts(page, action); })
        .catch((error) => {
            console.log(error);
        });
}