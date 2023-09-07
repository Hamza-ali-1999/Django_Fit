document.addEventListener('DOMContentLoaded', function() {
})

function create_entry(date){

    document.getElementById("entry-button").style.display = "none";

    var entry_input = document.createElement("form");
    entry_input.onsubmit = "return false;"

    entry_input.innerHTML = `
    
    <div class="form-group">
        <label for="entry-name">Entry Name</label>

        <input type="text" class="form-control" id="entry-name" aria-describedby="entryHelp" placeholder="Enter consumable name">

        <small id="entryHelp" class="form-text text-muted">The name or brand of food item, example: Mango, Coca Cola etc.</small>
    </div>
    
    <div class="form-group">
        <label for="entry-amount">Entry Amount</label>

        <input type="text" class="form-control" id="entry-amount" aria-describedby="amountHelp" placeholder="Enter consumable amount">

        <small id="amountHelp" class="form-text text-muted">The amount of the consumble in terms of count or measurement, example: for an entry of Mango --> 1, for an Entry of Coca Cola --> 200ml etc.</small>
    </div>
    
    <div class="form-group">
        <label for="entry-value">Entry Caloric Value</label>

        <input type="text" class="form-control" id="entry-value" aria-describedby="valueHelp" placeholder="Enter consumable caloric value">

        <small id="valueHelp" class="form-text text-muted">The caloric value for food item, example: for an entry of Mango --> 90, for an Entry of Coca Cola --> 175 etc.</small>
    </div>

    <div class="form-group">
        <label for="entry-date">Enter the date for the entry</label>
        <input type="date" class="form-control" id="entry-date">

    </div>
    
    <button type="submit" class="btn btn-primary">Submit</button>
    `

    document.getElementById("entry-form").append(entry_input)


    entry_input.addEventListener("submit", function(event){

        event.preventDefault();

        ent_name = document.getElementById("entry-name").value
        amount = document.getElementById("entry-amount").value
        value = document.getElementById("entry-value").value
        ent_date = document.getElementById("entry-date").value
        

        fetch(`/create_entry/${ent_name}/${amount}/${value}/${ent_date}`)
        .then(response => response.json())
        .then(entry =>{
            
            const name = entry.name 
            const value = entry.value
            const amount = entry.amount
            const id = entry.id

            console.log(ent_date)
            console.log(date)
            
            if(date == ent_date){

                const new_ent = document.createElement('div');
                new_ent.innerHTML=`
                
                <div class="row" id="${id}">
                
                    <div class="col" style="text-align: left; color: #ffffff;">
                        ${name}
                    </div>
                
                    <div class="col" style="text-align: right; color: #ffffff;">
                        ${amount}
                    </div>
                
                    <div class="col" style="text-align: right; color: #ffffff;">
                        ${value}
                    </div>

                    <div class="col">
                        <button type="button" onclick="remove(${id}, ${date})" class="close" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                
                </div>
                
                `
                document.getElementById("new_entries").append(new_ent)

                fetch(`update_meter/${date}`)
                .then((response) => response.json())
                .then((data)=>{

                    document.getElementById("meter").innerHTML=`
            
                    <svg width="250" height="250" viewBox="-31.25 -31.25 312.5 312.5" version="1.1" xmlns="http://www.w3.org/2000/svg" style="transform:rotate(-90deg)">
                        <circle r="115" cx="125" cy="125" fill="transparent" stroke="#e0e0e0" stroke-width="9" stroke-dasharray="722.2px" stroke-dashoffset="0"></circle>
                        <circle id="progress-meter" r="115" cx="125" cy="125" stroke="#1aff94" stroke-width="14" stroke-linecap="round" stroke-dashoffset="${data.total}px" fill="transparent" stroke-dasharray="722.2px"></circle>
                        <text id="progress-reading" x="75px" y="140px" fill="#1aff94" font-size="46px" font-weight="bold" style="transform:rotate(90deg) translate(0px, -246px)">${data.percent}%</text>
                    </svg>
            
                    `
                })
            }



            document.getElementById("entry-form").style.display = "none";
            document.getElementById("entry-button").style.display = "block";

            location.reload()
            

        })

    })
}


function remove(ID, date){

    fetch(`remove_entry/${ID}/${date}`)
    .then((response) => response.json())
    .then((data)=>{

        document.getElementById(`${ID}`).remove()

        document.getElementById("meter").innerHTML=`
        
        <svg width="250" height="250" viewBox="-31.25 -31.25 312.5 312.5" version="1.1" xmlns="http://www.w3.org/2000/svg" style="transform:rotate(-90deg)">
            <circle r="115" cx="125" cy="125" fill="transparent" stroke="#e0e0e0" stroke-width="9" stroke-dasharray="722.2px" stroke-dashoffset="0"></circle>
            <circle id="progress-meter" r="115" cx="125" cy="125" stroke="#1aff94" stroke-width="14" stroke-linecap="round" stroke-dashoffset="${data.total}px" fill="transparent" stroke-dasharray="722.2px"></circle>
            <text id="progress-reading" x="75px" y="140px" fill="#1aff94" font-size="46px" font-weight="bold" style="transform:rotate(90deg) translate(0px, -246px)">${data.percent}%</text>
        </svg>

        `

    })


}




function save(id){


    fetch(`workout_save/${id}`)
    .then((response) => response.json())
    .then((values)=>{

        console.log(id)
        console.log(values.reaction)

        if(values.reaction){
            document.getElementById(`button${id}`).innerHTML =`<button type="button" class="btn btn-primary btn-lg">Save</button>`
        }else{
            document.getElementById(`button${id}`).innerHTML =`<button type="button" class="btn btn-primary btn-lg" style="background-color: red;">Unsave</button>`
        }


    })




}


function delete_workout(id){

    fetch(`delete_workout/${id}`)
    .then((response) => response.json())
    .then((values)=>{

        if(values.reaction){
            document.getElementById(`entire_post${id}`).remove()
        }


    })

}