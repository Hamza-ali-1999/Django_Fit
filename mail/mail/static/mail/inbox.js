document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // **Compose Button
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;



  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {    
      emails.forEach(email => {

        const sender = email.sender;
        const time = email.timestamp;
        const subject = email.subject;
        const read = email.read;
        const id = email.id;

        const space = document.createElement('div');
        space.innerHTML=`<br>`;

        const mail_element = document.createElement('nav');
        mail_element.className = "navbar-nav mr-auto";
        mail_element.style = "border:1px solid #cecece; border-radius: 5px;"

        if(read=== true){
          mail_element.style = "border:1px solid #cecece; border-radius: 5px; background-color: LightGray"
        }

        mail_element.innerHTML = `
        <div class="container">
            <div class="row">
                <div class="col-sm-11">
                  <a style="text-decoration : none; color : #000000;">
                  From: <b>${sender}</b>, Subject: <b>${subject}</b>   
                  </a> 
                </div>
                <div class="col-sm-1" style="font-size:11px;">   
                  ${time} 
                </div>
            </div>
            </div>
        `;
        
        mail_element.addEventListener('click', () => email_page(id, mailbox));
        
        document.querySelector('#emails-view').append(space);
        document.querySelector('#emails-view').append(mail_element);
      })

  });

}

function email_page(email_id, mailbox){

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>From ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)} mail:</h3>`;
  
  //setting email read to true after it has openned
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
            read: true
    })
  })

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // variables
    const sender = email.sender;
    const time = email.timestamp;
    const subject = email.subject;
    const body = email.body;
    const recipients = email.recipients;
    var arch_bool = email.archived;

    const button1 = document.createElement('button');
    button1.className = "btn btn-sm btn-outline-primary";
    button1.type="button";
    const button2 = document.createElement('button');
    button2.className = "btn btn-sm btn-outline-primary";
    button2.type="button";

    const space = document.createElement('div');
    space.innerHTML=`<br>`;

    const mail_element = document.createElement('div');
    mail_element.className = "container-fluid";
    mail_element.style = "border:1px solid #cecece;"

    // individual mail html contents
    mail_element.innerHTML = `
          <br>  
          <div style="font-size:30px;">
          ${subject}
          </div>
          <br>

          <nav>
          <div>
            <div class="row">
                <div class="col-sm-10">
                  <div style="font-size:25px;"><b>${sender}</b></div>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-10">
                  <div style="font-size:15px">
                    To: ${recipients}
                  </div>
                </div>              
                <div class="col-sm-2" style="font-size:15px;">   
                    ${time} 
                </div>
            <div>
          </div>
          </nav>

          <br>
          <nav>
          <div class="container">
            <div class="row">
                <div class="col">
                  <div style="font-size:20px;">${body}</div>
                </div>
            </div>
          </div>
          </nav>
          <br><br>
    `;
   
    // Checking to see which inbox email is accessed
    if(arch_bool === true){
      button1.innerHTML=`Unarchive`;

      document.querySelector('#emails-view').append(mail_element);
      document.querySelector('#emails-view').append(space);
      document.querySelector('#emails-view').append(button1);
    }else if(arch_bool === false){
      button1.innerHTML=`Archive`;
      button2.innerHTML=`Reply`;
      document.querySelector('#emails-view').append(mail_element);
      document.querySelector('#emails-view').append(space);

      if(`${mailbox}` === "inbox"){
      document.querySelector('#emails-view').append(button1);
      document.querySelector('#emails-view').append(button2);
      }
    }

    // Archive/Unarchive Button
    button1.addEventListener('click', () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
                archived: !arch_bool
        })
      })
      load_mailbox("inbox");
      location.reload();
    })

    // Reply Button function
    button2.addEventListener('click', () => {
      compose_email();

      document.querySelector('#compose-recipients').value = sender;
      document.querySelector('#compose-subject').value = 'Re: '+ subject;
      document.querySelector('#compose-body').value = '"On ' + time + ', ' + sender + ' wrote: ' + body+'"'+'<br><br><br><br>';
    })

  })

}


function send_email(){

  // Takes Values from the Compose Form
  const body = document.querySelector('#compose-body').value;
  const sub = document.querySelector('#compose-subject').value;
  const rec = document.querySelector('#compose-recipients').value;
  
  // modified POST 
  fetch('/emails', {
    method: 'POST',
      body: JSON.stringify({
        recipients: rec,
        subject: sub,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent');
  });

  return false;
}


