
//Like Function
function like_switch(post_id){

    fetch(`/like_post/${post_id}`, {
        method: "POST",
    })
    .then((response) => response.json())
    .then((values) => {
    
        console.log(values.reaction)
        console.log(values.likecount)

        if(values.reaction){

            document.getElementById(`like_button${post_id}`).innerHTML = `
            <button class="btn btn-info" style="background-color: Red; color: White;">Unlike</button>
            `;

            document.getElementById(`like_count${post_id}`).innerHTML =`<div>Likes: ${values.likecount}</div>`

        }else{
            document.getElementById(`like_button${post_id}`).innerHTML = `
            <button class="btn btn-info">Like</button>
            `;

            document.getElementById(`like_count${post_id}`).innerHTML =`<div>Likes: ${values.likecount}</div>`
        }

    })



}


//Follow Function
function follow_switch(follow_id){

    fetch(`/follow_user/${follow_id}`, {
        method: "POST",
    })
    .then((response) => response.json())
    .then((values) => {

        console.log(values.reaction)
        console.log(values.followcount)
        console.log(values.following)


        if(values.reaction == null){

            document.querySelector(`#follow-button`).innerHTML = `
            <div>Followers: ${values.followcount}</div>
            <div>Following: ${values.following}</div>
            `;

        }else if(values.reaction){

            document.querySelector(`#follow-button`).innerHTML = `
            <button type="button" class="btn btn-outline-primary" style="background-color: Red; color: White;">Unfollow</button>
            `;
            
            document.querySelector(`#follow_numbers`).innerHTML = `
            <div>Followers: ${values.followcount}</div>
            <div>Following: ${values.following}</div>
            `;


        }else{
            document.querySelector(`#follow-button`).innerHTML = `
            <button type="button" class="btn btn-outline-primary">Follow</button>
            `;

            document.querySelector(`#follow_numbers`).innerHTML = `
            <div>Followers: ${values.followcount}</div>
            <div>Following: ${values.following}</div>
            `;
        }
    })


}


//Following Page Function
function following_page(){

    fetch(`/logged_user`)
    .then(response => response.json())
    .then(logged_user => {

        const logged_userID = logged_user.ID;

        fetch(`/posts/${postbox}`)
            .then(response => response.json())
            .then(posts => {
                posts.forEach(post => {


                    //data values
                    const user = post.name;
                    const time = post.date;
                    const post_maker = post.poster;
                    const text = post.post;
                    const userID = post.user_id;
                    const like_id = post.id;
                    const like_count = post.likes.length;
                    const likers = post.likes;

                    //creating elements
                    const space = document.createElement('div');
                    space.innerHTML=`<br>`;

                    const post_element = document.createElement('div');
                    post_element.innerHTML =`

                    <div class="jumbotron">
                        <div>
                            <div class="row">
                                <div class="col-sm-1">
                                    <b>
                                        <a>${user}</a>
                                    </b>
                                </div>
                                <div class="col-sm-11">
                                <div>|| ${post_maker} || ${time}
                                </div>
                            </div>
                            <hr>
                            <div>
                                ${text}
                            </div>
                        </div>
                    </div>
                    `

                    const like_button = document.createElement('div');

                    //Event Listeners        
                    post_element.addEventListener('click',()=> load_profile(userID))
                    //Appending posts and buttons
                    document.querySelector('#allposts').append(post_element);


                    if(userID == logged_userID){
                        document.querySelector('#allposts').append(space);
                    }else if(likers.includes(logged_userID)){

                        like_button.innerHTML=`
                        <div  id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                            <button class="btn btn-info" style="background-color: Red; color: White;">
                            <div style="font-size:13px;">Unlike</div>
                            </button>
                            <div style="font-size:13px;">Likes: ${like_count}</div>
                        </div>
                        `

                        like_button.addEventListener('click',()=> like_switch(like_id));

                        document.querySelector('#allposts').append(like_button);

                    }else{
                        like_button.innerHTML=`
                            <div id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                                <button class="btn btn-info">
                                <div style="font-size:13px;">Like</div>
                                </button>
                                <div style="font-size:13px;">Likes: ${like_count}</div>
                            </div>
                            `
                        like_button.addEventListener('click',()=> like_switch(like_id));
                        
                        document.querySelector('#allposts').append(like_button);

                    }


                })
            })

    })

//function end
}


//Test
function textarea(ID){
    
    const text_ID = 'text'+ ID

    let space_text = document.getElementById(text_ID).textContent;

    var text_input = document.createElement("form");
    text_input.onsubmit = "return false;"

    //modify this
    const form_ID = 'form'+ ID;
    const textareaID = 'textarea'+ID;
    const edit_buttonID = 'edit_button'+ID;
    const edit_status = 'edit_status'+ID;

   
    const space_textID = 'spacetext'+ID;

    text_input.id= form_ID;

    text_input.innerHTML=`
    <div class="form-group">
        <textarea class="form-control" rows="3" maxlength="320" cols="200" id="${space_textID}"></textarea>
    </div>
    <input type="submit" class="btn btn-primary">
    `

    //sets existing post text to null
    document.getElementById(text_ID).innerHTML =``;
    document.getElementById(text_ID).style.display = "none";
    document.getElementById(edit_buttonID).style.display = "none";

    //appends and fills textarea with previous post text
    document.getElementById(textareaID).append(text_input);
    //make sure that the post text does not have extra line skips and spaces
    document.getElementById(space_textID).innerHTML = space_text;

    //adding eventlistener to form element: text_input
    text_input.addEventListener("submit", function(event) {
        


        event.preventDefault();
        new_text = document.getElementById(space_textID).value;

        



        fetch(`/edit_post/${ID}/${new_text}`,{
            method: "POST",
            body: JSON.stringify({
                post_text: new_text,
            }),
        })
        .then(response => response.json())
        .then(post => {

            document.getElementById(text_ID).innerHTML = post.post ;
            document.getElementById(text_ID).style.display = "block";
            document.getElementById(edit_status).innerHTML = ` ** Edited ** ` ;
            document.getElementById(edit_buttonID).style.display = "block";
            document.getElementById(form_ID).remove();


        });


    })
}



//  TOD0: Using a new API route update the text and innerHTML of post using post_ID
function edit_post(post_ID, new_text){



}











//
//
// Inactive Functions for API routes previously used for testing
// Functions are ignored 
//
//





//Load All Posts
function load_postbox(postbox, page){
    
    window.scrollTo(0,0);
    document.querySelector('#allposts').innerHTML =``;
    document.getElementById("page_number").innerHTML = `Current Page: ${page}`

    const next_button = document.getElementById("next-button");
    const prev_button = document.getElementById("previous-button");

    next_button.style.visibility = "visible";
    prev_button.style.visibility = "visible";

    fetch(`/logged_user`)
    .then(response => response.json())
    .then(logged_user => {

        const logged_userID = logged_user.ID;

        fetch(`/posts/${postbox}/${page}`)
        .then(response => response.json())
        .then(posts => {

            const page_posts = posts.length
            const x = page_posts - 10;


            const int = 1;

            prev_page = +page - int;
            next_page = +page + int;
            

            
            if(page == 1){
                prev_button.style.visibility = "hidden";
            }else if(x < 0 ){
                next_button.style.visibility = "hidden";
            }

            next_button.addEventListener('click',()=>{
                load_postbox('allposts', next_page)
            });
            
            prev_button.addEventListener('click',()=>{
                load_postbox('allposts', prev_page)
            });


            posts.forEach(post => {

                //data values
                const user = post.name;
                const time = post.date;
                const post_maker = post.poster;
                const text = post.post;
                const userID = post.user_id;
                const like_id = post.id;
                const like_count = post.likes.length;
                const likers = post.likes;

                //creating elements
                const space = document.createElement('div');
                space.innerHTML=`<br>`;

                const post_element = document.createElement('div');
                post_element.setAttribute('id', like_id);
                post_element.innerHTML =`

                <div class="jumbotron">
                    <div>
                        <div class="row">
                            <div class="col-sm-1">
                                <b>
                                    <a>${user}</a>
                                </b>
                            </div>
                            <div class="col-sm-11">
                            <div>|| ${post_maker} || ${time}
                            </div>
                        </div>
                        <hr>
                        <div>
                            ${text}
                        </div>
                    </div>
                </div>
                `

                const like_button = document.createElement('div');

                //Event Listeners        
                post_element.addEventListener('click',()=> load_profile(userID))
                //Appending posts and buttons
                document.querySelector('#allposts').append(post_element);


                if(userID == logged_userID){
                    document.querySelector('#allposts').append(space);

                }else if(likers.includes(logged_userID)){

                    like_button.innerHTML=`
                    <div  id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                        <button class="btn btn-info" style="background-color: Red; color: White;">
                        <div style="font-size:13px;">Unlike</div>
                        </button>
                        <div style="font-size:13px;">Likes: ${like_count}</div>
                    </div>
                    `

                    like_button.addEventListener('click',()=> like_switch(like_id));

                    document.querySelector('#allposts').append(like_button);

                }else{
                    like_button.innerHTML=`
                        <div id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                            <button class="btn btn-info">
                            <div style="font-size:13px;">Like</div>
                            </button>
                            <div style="font-size:13px;">Likes: ${like_count}</div>
                        </div>
                        `
                    like_button.addEventListener('click',()=> like_switch(like_id));
                    
                    document.querySelector('#allposts').append(like_button);

                    

                }
            })
            
            console.log(posts);
            


        });

    });

    

}

//Load Profile Pagee
function load_profile(user_id){

    document.querySelector('#allposts').innerHTML = '';

    // Profile Heading //
    fetch(`/list/${user_id}`)
    .then(response => response.json())
    .then(list => {


            const profile_name = list.user
            const followers = list.followers
            const following = list.following

            profile_followers_count = followers.length
            profile_following_count = following.length

            document.getElementById("title").innerHTML=`${profile_name}`



            // Follow Button //
            fetch(`/logged_user`)
            .then(response => response.json())
            .then(logged_user => {

                
                const logged_userID = logged_user.ID;

                //Follow Button
                if(list.ID == logged_userID){

                    follow_switch(logged_userID)

                }else if(followers.includes(logged_userID)){

                    document.getElementById("follow-button").innerHTML=`
                    <button type="button" class="btn btn-outline-primary" style="background-color: Red; color: White;">Unfollow</button>
                    <div>Followers: ${profile_followers_count}</div>
                    <div>Following: ${profile_following_count}</div>
                    `
                    document.getElementById("follow-button").addEventListener('click',()=> follow_switch(user_id));
                
                }else{

                    document.getElementById("follow-button").innerHTML=`
                    <button type="button" class="btn btn-outline-primary">Follow</button>
                    <div>Followers: ${profile_followers_count}</div>
                    <div>Following: ${profile_following_count}</div>
                    `
                    document.getElementById("follow-button").addEventListener('click',()=>follow_switch(user_id));

                }


                fetch(`/profile_posts/${user_id}`)
                .then(response => response.json())
                .then(profile_posts =>{

                    profile_posts.forEach(profile_post =>{
                    
                    //Data values
                    const user = profile_post.name;
                    const time = profile_post.date;
                    const post_maker = profile_post.poster;
                    const text = profile_post.post;
                    const like_count = profile_post.likes.length;
                    const like_id = profile_post.id;
                    const likers = profile_post.likes;
                    const userID = profile_post.user_id;

                    //Creating elements//
                    const like_button = document.createElement('div');
                    const space = document.createElement('div');
                    space.innerHTML=`<br>`;

                    const post_element = document.createElement('div');
                    post_element.innerHTML =`

                    <div class="jumbotron">
                        <div>
                            <div class="row">
                                <div class="col-sm-1">
                                    <b>
                                        <a>${user}</a>
                                    </b>
                                </div>
                                <div class="col-sm-11">
                                <div>|| ${post_maker} || ${time}</div> 
                                </div>
                            </div>
                            <hr>
                            <div>
                                ${text}
                            </div>
                        </div>
                    </div>
                    `
                    document.querySelector('#allposts').append(post_element);
                    
                    if(userID == logged_userID){
                        document.querySelector('#allposts').append(space);
                    }else if(likers.includes(logged_userID)){
    
                        like_button.innerHTML=`
                        <div  id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                            <button class="btn btn-info" style="background-color: Red; color: White;">
                            <div style="font-size:13px;">Unlike</div>
                            </button>
                            <div style="font-size:13px;">Likes: ${like_count}</div>
                        </div>
                        `
    
                        like_button.addEventListener('click',()=> like_switch(like_id));
    
                        document.querySelector('#allposts').append(like_button);
    
                    }else{
                        like_button.innerHTML=`
                            <div id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                                <button class="btn btn-info">
                                <div style="font-size:13px;">Like</div>
                                </button>
                                <div style="font-size:13px;">Likes: ${like_count}</div>
                            </div>
                            `
                        like_button.addEventListener('click',()=> like_switch(like_id));
                        
                        document.querySelector('#allposts').append(like_button);
    
                    }

                    })
                });

        });        
    })
}

//Following Page Function
function following_page(postbox){


    document.querySelector('#allposts').innerHTML = '';
    document.querySelector('#title').innerHTML = 'Following Page';
    document.querySelector('#follow-button').innerHTML = '';
    


    fetch(`/logged_user`)
    .then(response => response.json())
    .then(logged_user => {

        const logged_userID = logged_user.ID;

        fetch(`/posts/${postbox}`)
            .then(response => response.json())
            .then(posts => {
                posts.forEach(post => {


                    //data values
                    const user = post.name;
                    const time = post.date;
                    const post_maker = post.poster;
                    const text = post.post;
                    const userID = post.user_id;
                    const like_id = post.id;
                    const like_count = post.likes.length;
                    const likers = post.likes;

                    //creating elements
                    const space = document.createElement('div');
                    space.innerHTML=`<br>`;

                    const post_element = document.createElement('div');
                    post_element.innerHTML =`

                    <div class="jumbotron">
                        <div>
                            <div class="row">
                                <div class="col-sm-1">
                                    <b>
                                        <a>${user}</a>
                                    </b>
                                </div>
                                <div class="col-sm-11">
                                <div>|| ${post_maker} || ${time}
                                </div>
                            </div>
                            <hr>
                            <div>
                                ${text}
                            </div>
                        </div>
                    </div>
                    `

                    const like_button = document.createElement('div');

                    //Event Listeners        
                    post_element.addEventListener('click',()=> load_profile(userID))
                    //Appending posts and buttons
                    document.querySelector('#allposts').append(post_element);


                    if(userID == logged_userID){
                        document.querySelector('#allposts').append(space);
                    }else if(likers.includes(logged_userID)){

                        like_button.innerHTML=`
                        <div  id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                            <button class="btn btn-info" style="background-color: Red; color: White;">
                            <div style="font-size:13px;">Unlike</div>
                            </button>
                            <div style="font-size:13px;">Likes: ${like_count}</div>
                        </div>
                        `

                        like_button.addEventListener('click',()=> like_switch(like_id));

                        document.querySelector('#allposts').append(like_button);

                    }else{
                        like_button.innerHTML=`
                            <div id="like_button${like_id}" align="right" style="padding-right:0.5cm; font-size:2px; padding-top:1px;">
                                <button class="btn btn-info">
                                <div style="font-size:13px;">Like</div>
                                </button>
                                <div style="font-size:13px;">Likes: ${like_count}</div>
                            </div>
                            `
                        like_button.addEventListener('click',()=> like_switch(like_id));
                        
                        document.querySelector('#allposts').append(like_button);

                    }


                })
            })

    })

//function end
}