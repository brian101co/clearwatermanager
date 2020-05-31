window.onload = () => {
    let lotNodes = document.querySelectorAll("[data-site]");
    let siteNodes = document.querySelectorAll(".site");
    let checkoutNodes = document.querySelectorAll(".checkout");
    let checkinNodes = document.querySelectorAll(".checkin");
    let editBtn = document.querySelector('.edit');
    let closeEdit = document.querySelectorAll('.close-edit');

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
    let editModalHeader = document.querySelector('.edit-header h5');
    let id;

    names.forEach(name => {
        name.addEventListener('click', (event) => {
            id = parseInt(event.target.parentElement.previousElementSibling.innerText);
            document.querySelector('.delete-form').setAttribute("action", `delete/${id}`);
        })
    });

    editBtn.addEventListener('click', () => {
        document.querySelector('.delete-form').classList.toggle('d-none');
        editModalHeader.innerHTML = "Edit Reservation";
        let editForm = document.querySelector('.edit-form');
        editForm.classList.toggle('d-none');
        editForm.setAttribute("action", `edit/${id}`);

        let url = window.location.origin + "/reservation/" + id;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                editForm.querySelector('[name="name"]').value = data[0].title;
                editForm.querySelector('[name="lot"]').value = data[0].site;
                editForm.querySelector('[name="phone"]').value = data[0].phoneNum;
            })
            .catch(err => console.log(err));
    });

    closeEdit.forEach(elem => {
        elem.addEventListener('click', () => {
            editModalHeader.innerHTML = "Delete Reservation"
            setTimeout(() => {
                document.querySelector('.delete-form').classList.toggle('d-none');
                document.querySelector('.edit-form').classList.toggle('d-none');
            }, 300);
        });
    });
}



