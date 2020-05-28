window.onload = () => {
    let lotNodes = document.querySelectorAll("[data-site]");
    let siteNodes = document.querySelectorAll(".site");
    let checkoutNodes = document.querySelectorAll(".checkout");
    let checkinNodes = document.querySelectorAll(".checkin");

    let currentTime = Date.now()
    
    let activelots = [];
    
    for (let i = 0; i < siteNodes.length; i++) {
        let obj = {};
        obj.site = siteNodes[i].innerText;
        obj.checkout = checkoutNodes[i].innerText;
        obj.checkin = checkinNodes[i].innerText;
        activelots.push(obj);
    }

    lotNodes.forEach(lot => {
        let lotNum = lot.getAttribute("data-site"); 
        let search = activelots.find(element => element.site == lotNum);
        
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
            document.querySelector('.delete-form').setAttribute("action", `dashboard/delete/${id}`);
        })
    });
    
}



