document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => { load_mailbox('inbox') });
  document.querySelector('#sent').addEventListener('click', () => { load_mailbox('sent') });
  document.querySelector('#archived').addEventListener('click', () => { load_mailbox('archive') });
  document.querySelector('#compose').addEventListener('click', () => { compose_email() });

  // By default, load the inbox
  load_mailbox('inbox');

  const form = document.getElementsByTagName('form')[0]
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    form.classList.add('was-validated');
    if (form.checkValidity()) {
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
          recipients: document.getElementById('compose-recipients').value,
          subject: document.getElementById('compose-subject').value,
          body: document.getElementById('compose-body').value.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp'),
        }),
      })
        .then((response) => {
          if (response.status === 201) {
            form.classList.remove('was-validated');
            load_mailbox('inbox');
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
          setTimeout(() => { alert.remove(); }, 10000);
        });
    } else {
       event.stopPropagation();
    }
  })
});

function compose_email(recipients = '', subject = '', body = '') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body.replace(/<br>/g, '\n').replace(/&nbsp/g, '\t');
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';

  // Show the mailbox name
  const emailList = document.querySelector('#emails-view')
  emailList.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      for (let email of emails) {
        const emailDiv = document.createElement('div');
        emailDiv.addEventListener('click', () => {show_email(email.id) });
        emailDiv.classList.add('email');
        if (email.read) {
          emailDiv.classList.add('read');
        }

        const sender = document.createElement('h5');
        sender.innerHTML = `<b>From</b>: ${email.sender}`;
        emailDiv.appendChild(sender);
        
        const timestamp = document.createElement('p');
        timestamp.innerHTML = `${email.timestamp}`;
        timestamp.classList.add('timestamp', 'mb-4');
        emailDiv.appendChild(timestamp);

        const subject = document.createElement('div');
        subject.innerHTML = `<b>Subject</b>: ${email.subject}`;
        emailDiv.appendChild(subject);

        emailList.appendChild(emailDiv);
      }
    })
}

function show_email(email_id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'block';

  let user = document.getElementById('user');
  let archiveBtn = removeEventListeners('archive');
  let replyBtn = removeEventListeners('reply');
    
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      document.getElementsByClassName('from')[0].innerHTML = `<b>From</b>: ${email.sender}`;
      document.getElementsByClassName('to')[0].innerHTML = `<b>To</b>: ${email.recipients.join(', ')}`;
      document.getElementsByClassName('subject')[0].innerHTML = `<b>Subject</b>: ${email.subject}`;
      document.getElementsByClassName('time')[0].innerHTML = `<b>Datetime</b>: ${email.timestamp}`;
      document.getElementsByClassName('content')[0].innerHTML = `${email.body}`;
      
      if (email.sender === user.innerText) {
        archiveBtn.style.display = 'none';
        replyBtn.style.display = 'none';
      } else {
        archiveBtn.innerText = email.archived ? 'Unarchive' : 'Archive';
        archiveBtn.style.display = 'block';
        replyBtn.style.display = 'block';
        archiveBtn.addEventListener('click', () => archive(email));
      }
      let body = email.body.split('<br>').map(line => `\t${line}`).join('\n');
      replyBtn.addEventListener('click', () => compose_email(email.sender, `Re: ${email.subject.replace(/Re: /g, '')}`, `On ${email.timestamp} ${email.sender} wrote:\n${body}\n\n`));

      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true,
          })
        })
      }
    })
}

function removeEventListeners(element_id) {
  let oldArchiveBtn = document.getElementById(element_id);
  let newArchiveBtn = oldArchiveBtn.cloneNode(true);
  oldArchiveBtn.parentNode.replaceChild(newArchiveBtn, oldArchiveBtn);
  return newArchiveBtn;
}

async function archive(email) {
  await fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived,
    }),
  });

  load_mailbox('inbox');
}