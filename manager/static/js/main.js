window.onload = () => {
    const lotNodes = document.querySelectorAll("[data-site]");
    const siteNodes = document.querySelectorAll(".site");
    const checkoutNodes = document.querySelectorAll(".checkout");
    const checkinNodes = document.querySelectorAll(".checkin");
    const editBtn = document.querySelector('.edit');
    const closeEdit = document.querySelectorAll('.close-edit');
    const currentTime = Date.now();
    const names = document.querySelectorAll('.name');
    const editModalHeader = document.querySelector('.edit-header h5');
    let id;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    class Map {
        constructor(mapLots, reservedLots, checkout, checkin) {
            this.mapLots = mapLots;
            this.reservedLots = reservedLots;
            this.checkoutTimes = checkout;
            this.checkinTimes = checkin;
            this.activelots = [];
            this.infoModal = document.querySelector("#site-info");
            this.setEventListeners();
        }

        setEventListeners() {
            this.mapLots.forEach(lot => {
                const siteNumber = lot.getAttribute("data-site");
                lot.addEventListener("click", (e) => {
                    const url = window.location.origin + "/site/info/" + siteNumber;
                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            this.infoModal.querySelector(".modal-title").innerText = `Site ${data[0].identifier}`;
                            this.infoModal.querySelector(".content").innerText = data[0].info;
                            this.infoModal.querySelector(".content").setAttribute("site", data[0].identifier);
                        })
                        .catch(err => {
                            this.infoModal.querySelector(".modal-title").innerText = `Site ${siteNumber}`;
                            this.infoModal.querySelector(".content").setAttribute("site", siteNumber);
                            this.infoModal.querySelector(".content").innerText = "No information available.";
                        });
                    
                });
            });

            this.infoModal.querySelector(".modal-body").addEventListener("click", (e) => {
                if (e.target.classList.contains("save")) {
                    const siteInfoText = e.currentTarget.querySelector(".content").innerText;
                    const siteNumber = e.currentTarget.querySelector(".content").getAttribute("site");
                    const url = window.location.origin + "/site/info/" + siteNumber;
                    console.log(JSON.stringify({"info": siteInfoText}))
                    fetch(url, {
                        method: "POST",
                        headers: {
                            "Accept": "application/json",
                            "X-CSRFToken": csrftoken
                        },
                        body: JSON.stringify({"info": siteInfoText})
                    }).then(response => response.json())
                    .then(data => {
                        console.log(data);
                    })
                    .catch(err => {
                        console.log(err);
                    });
                }
            });
        }

        buildReservedLots() {
            // Building an Array of active lots based on current reservations in the reservation table
            for (let i = 0; i < this.reservedLots.length; i++) {
                let obj = {};
                obj.site = this.reservedLots[i].innerText;
                obj.checkout = this.checkoutTimes[i].innerText;
                obj.checkin = this.checkinTimes[i].innerText;
                this.activelots.push(obj);
            }
        }

        highlightLots() {
            this.buildReservedLots();
            // Looping through each lot on the map
            this.mapLots.forEach(lot => {
                // Lot Number
                let lotNum = lot.getAttribute("data-site");
                // Checking if lot number is in the active lots array to see if it needs to be highlighted
                let filterdActiveLots = this.activelots.filter(elem => elem.site == lotNum);

                let search;
                if (filterdActiveLots.length == 1) {
                    search = this.activelots.find(element => {
                        return element.site == lotNum;
                    });
                } else {
                    filterdActiveLots.forEach(lot => {
                        if (dateFns.isAfter(lot.checkout, currentTime)) {
                            if (dateFns.isBefore(lot.checkin, currentTime)) {
                                document.querySelector(`[data-site="${lot.site}"]`).setAttribute("id", "active");
                            }
                        }
                    });
                }

                if (search) {
                    if (dateFns.isAfter(search.checkout, currentTime)) {
                        if (dateFns.isBefore(search.checkin, currentTime)) {
                            document.querySelector(`[data-site="${search.site}"]`).setAttribute("id", "active");
                        }
                    }
                }
            });
        }
    }

    class Modal {
        constructor(obj) {
            this.config = obj;
        }

        addDeleteFunctionality() {
            this.config.deleteElem.forEach(name => {
                name.addEventListener('click', (event) => {
                    id = parseInt(event.target.parentElement.previousElementSibling.previousElementSibling.innerText);
                    document.querySelector('.delete-form').setAttribute("action", `delete/${id}`);
                })
            });
        }

        addEditFunctionality() {
            this.config.editElem.addEventListener('click', () => {
                document.querySelector('.delete-form').classList.toggle('d-none');
                editModalHeader.innerHTML = "Edit Reservation";
                let editForm = document.querySelector('.edit-form');
                editForm.classList.toggle('d-none');
                editForm.setAttribute("action", `edit/${id}`);

                let url = window.location.origin + "/api/reservation/" + id;
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        editForm.querySelector('[name="name"]').value = data[0].title;
                        editForm.querySelector('[name="lot"]').value = data[0].site;
                        editForm.querySelector('[name="phone"]').value = data[0].phoneNum;
                        editForm.querySelector('[name="checkin"]').value = data[0].start.slice(0, -1);
                        editForm.querySelector('[name="checkout"]').value = data[0].end.slice(0, -1);
                    })
                    .catch(err => console.log(err));
            });
        }

        addCloseEditFunctionality() {
            this.config.closeElem.forEach(elem => {
                elem.addEventListener('click', () => {
                    editModalHeader.innerHTML = "Delete Reservation"
                    setTimeout(() => {
                        document.querySelector('.delete-form').classList.toggle('d-none');
                        document.querySelector('.edit-form').classList.toggle('d-none');
                    }, 300);
                });
            });
        }

    }

    class Notification {
        constructor(obj) {
            this.config = obj;
        }

        getNotifications() {
            fetch(this.config.url)
                .then(response => response.json())
                .then(data => {
                    if (data.length == 0) {
                        document.querySelector('.notifications-container').innerHTML += `<div class="alert alert-secondary mt-1" role="alert">
                                                                                                No campers checking out tomorrow.
                                                                                        </div>`;
                    } else {
                        data.forEach(reservation => {
                            let time = new Date(reservation.end);
                            document.querySelector('.notifications-container').innerHTML += `<div class="alert alert-primary mt-1" role="alert">
                                                                                                <strong>${reservation.title}</strong> | Site: ${reservation.site} | Checkout: ${time.toDateString()}
                                                                                            </div>`;
                        });
                    }
                })
                .catch(err => console.log(err));
        }
    }

    const NewMap = new Map(lotNodes, siteNodes, checkoutNodes, checkinNodes);
    const Notifications = new Notification({
        url: window.location.origin + "/api/notifications/",
    });
    const InitModal = new Modal({
        deleteElem: names,
        editElem: editBtn,
        closeElem: closeEdit,
    });

    NewMap.highlightLots();
    Notifications.getNotifications();
    InitModal.addDeleteFunctionality();
    InitModal.addEditFunctionality();
    InitModal.addCloseEditFunctionality();

}
