window.onload = () => {
    let lotNodes = document.querySelectorAll("[data-site]");
    let siteNodes = document.querySelectorAll(".site");
    let checkoutNodes = document.querySelectorAll(".checkout");
    let checkinNodes = document.querySelectorAll(".checkin");

    let currentTime = Date.now()
    
    let activelots = [];
    
    // Building an Array of active lots based on current reservations in the reservation table
    for (let i = 0; i < siteNodes.length; i++) {
        let obj = {};
        obj.site = siteNodes[i].innerText;
        obj.checkout = checkoutNodes[i].innerText;
        obj.checkin = checkinNodes[i].innerText;
        activelots.push(obj);
    }

    // Looping through each lot on the map
    lotNodes.forEach(lot => {
        // Lot Number
        let lotNum = lot.getAttribute("data-site"); 
        // Checking if lot number is in the active lots array to see if it needs to be highlighted
        let search = activelots.find(element => {
            return element.site == lotNum
        });
        
        if (search) {
            if ( dateFns.isAfter(search.checkout, currentTime) ) {
                if ( dateFns.isBefore(search.checkin, currentTime) ) {
                    document.querySelector(`[data-site="${search.site}"]`).setAttribute("id", "active");
                } 
            }   
        }
    });

    let names = document.querySelectorAll('.name');

    names.forEach(name => {
        name.addEventListener('click', (event) => {
            let id = parseInt(event.target.parentElement.previousElementSibling.innerText);
            document.querySelector('.delete-form').setAttribute("action", `delete/${id}`);
        })
    });
}



