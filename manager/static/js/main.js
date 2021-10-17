window.onload = () => {
    const lotNodes = document.querySelectorAll("[data-site]");
    const siteNodes = document.querySelectorAll(".site");
    const checkoutNodes = document.querySelectorAll(".checkout");
    const checkinNodes = document.querySelectorAll(".checkin");
    const editBtn = document.querySelector('.edit');
    const currentTime = Date.now();
    const names = document.querySelectorAll('.name');
    const mobileEditBtnElems = document.querySelectorAll(".mobile-edit");

    const state = {
        activeSiteId: null,
    }

    function showLoader(className, clearInfo=true) {
        if (clearInfo == true) {
            document.querySelector(".info-model-body .content").innerText = "";
        }
        const loaderContainer = document.createElement('div');
        loaderContainer.classList.add("d-flex", "justify-content-center", "loader-container");
        loaderContainer.innerHTML = `<div class="spinner-grow text-primary" role="status">
                                       <span class="sr-only">Loading...</span>
                                     </div>`;
        document.querySelector(className).prepend(loaderContainer);
    }

    function removeLoader(className) {
        const cln = className + " .loader-container";
        document.querySelector(cln).remove();
    }

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
                    showLoader(".info-model-body");
                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            removeLoader(".info-model-body");
                            this.infoModal.querySelector(".modal-title").innerText = `Site ${data[0].identifier}`;
                            this.infoModal.querySelector(".content").innerText = data[0].info;
                            this.infoModal.querySelector(".content").setAttribute("site", data[0].identifier);
                        })
                        .catch(err => {
                            removeLoader(".info-model-body");
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
            this.setEventListeners();
        }

        setEventListeners() {
            this.config.deleteElem.forEach(name => {
                name.addEventListener("click", (event) => {
                    state.activeSiteId = event.target.dataset.id;
                    document.querySelector('.delete-form').setAttribute("action", `delete/${state.activeSiteId}`);
                    document.querySelector('#reservation-detail').setAttribute("href", `reservation/${state.activeSiteId}`)
                });
            });
            this.config.editElem.addEventListener("click", (event) => {
                const form = document.querySelector('.edit-form');
                const url = window.location.origin + "/api/reservation/" + state.activeSiteId;
                form.setAttribute("action", `edit/${state.activeSiteId}`);
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        form.querySelector('[name="name"]').value = data[0].name;
                        form.querySelector('[name="lot"]').value = data[0].site;
                        form.querySelector('[name="phone"]').value = data[0].phoneNum;
                        form.querySelector('[name="info"]').value = data[0].info;
                        form.querySelector('[name="checkin"]').value = data[0].start.slice(0, -1);
                        form.querySelector('[name="checkout"]').value = data[0].end.slice(0, -1);
                    })
                    .catch(err => console.log(err));
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
                                                                                                <strong>${reservation.name}</strong> | Site: ${reservation.site} | Checkout: ${time.toDateString()}
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
        mobileEditBtnElems: mobileEditBtnElems,
    });

    NewMap.highlightLots();
    Notifications.getNotifications();

}
