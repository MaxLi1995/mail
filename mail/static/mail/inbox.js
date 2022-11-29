document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').onsubmit = () => {

    sendEmail();

  };
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';


  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    let text = "<ul style='list-style-type:none;display:block;'>";
    for (let i in emails) {
        text += `<li style='height:30px;width:100%;display:flex;border-style:solid;border-width:thin;margin:10px 0px;'>
        <div onclick='showEmail(${emails[i].id})' id='m${emails[i].id}' class='emails'`+ (emails[i].read ? "style='background-color:grey;'>" : ">") + 
        "<div style='position:absolute;text-align:left'>From: "
        + emails[i].sender +'</div><div style="position:absolute;left:40%;text-align:center;">Subject: ' + emails[i].subject + "</div><div style='position:absolute;left:75%'>"+ emails[i].timestamp
        + "</div></div></li>";
    }
    text += "</ul>";
    document.getElementById("emails-view").innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>` + text;

  });
}

function showEmail(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {

    document.querySelector('#sender').value = email.sender;
    document.querySelector('#reciver').value = email.recipients;
    document.querySelector('#title').value = email.subject;
    document.querySelector('#time').innerHTML = 'recived on: ' + email.timestamp;
    document.querySelector('#info').innerHTML = email.body;
    document.querySelector('#reply').addEventListener('click', () => reply(id));
    if (email.archived) {
      document.querySelector('#archive').innerHTML = 'Unarchive'
    } else {
      document.querySelector('#archive').innerHTML = 'Archive'
    };
    document.querySelector('#archive').addEventListener('click', () => archive(id, email.archived));
  
  });

  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
}

function archive(id, isArchived){
  fetch('/emails/' + id , {
    method: 'PUT',
    body: JSON.stringify({
        archived: !isArchived
    })
  });
  window.location.reload(true);

}


function reply(id) {
  compose_email();

  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {

    document.querySelector('#compose-recipients').value = email.sender;

    if (email.subject.includes("RE:")) {
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = 'RE: ' + email.subject;
    };
    
    document.getElementById("compose-body").value = 'On '+email.timestamp + ' ' + email.sender + ' wrote: ' + email.body;

  });
}

function sendEmail() {
  fetch('/emails', {
  
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
}