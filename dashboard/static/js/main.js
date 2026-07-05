const amenities = {
    electric_30amp: "30 AMP",
    electric_50amp: "50 AMP",
    water: "Water",
    sewer: "Sewer",
    wifi: "WiFi",
};

function createLoaderElem() {
    const containerElem = document.createElement("div");
    const loaderElem = document.createElement("div");
    const screenReaderElem = document.createElement("span");

    containerElem.classList.add("d-flex", "justify-content-center", "loader-container");
    screenReaderElem.classList.add("sr-only");
    loaderElem.classList.add("spinner-grow", "text-primary");
    loaderElem.setAttribute("role", "status");
    screenReaderElem.innerText = "Loading...";
    
    containerElem.appendChild(loaderElem);
    loaderElem.appendChild(screenReaderElem);
    return containerElem;
}

function showLoader(className, clearInfo=true) {
    if (clearInfo == true) {
        document.querySelector(".info-model-body .content").innerText = "";
    }
    document.querySelector(className).prepend(createLoaderElem());
}

function removeLoader(className) {
    const cln = className + " .loader-container";
    const loader = document.querySelector(cln);
    if (loader) loader.remove();
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

function createBadge(badgeType, text, extraClasses=[]) {
    const badgeElem = document.createElement("span");
    badgeElem.classList.add("badge", badgeType);
    if (extraClasses.length) {
        for (const cls of extraClasses) {
            badgeElem.classList.add(cls);
        }
    }
    badgeElem.innerText = text;
    return badgeElem;
}

function createListItem(text, childElem, extraClasses = []) {
    const listItemElem = document.createElement("li");
    listItemElem.classList.add("list-group-item");
    listItemElem.innerText = text;

    if (extraClasses.length) {
        listItemElem.classList.add(...extraClasses);
    }

    listItemElem.appendChild(childElem);
    return listItemElem;
}

function formatDateTime(dateInput) {
    const date = new Date(dateInput);
    return date.toLocaleString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        timeZone: "UTC",
    });
}

function createReservationCard(reservation_obj, lotNum) {
    const reservation = reservation_obj.fields;
    const pk = reservation_obj.pk;

    const cardElem = document.createElement("div");
    cardElem.classList.add("card", "shadow-sm", "mb-2");

    const cardBodyElem = document.createElement("div");
    cardBodyElem.classList.add("card-body", "py-3", "d-flex", "justify-content-between", "align-items-center", "flex-wrap");
    cardElem.appendChild(cardBodyElem);

    // Left — Reservation Info
    const leftElem = document.createElement("div");

    const nameLink = document.createElement("a");
    nameLink.href = `/reservations/${pk}`;
    nameLink.classList.add("text-dark", "font-weight-bold");
    nameLink.innerText = reservation.name;
    leftElem.appendChild(nameLink);

    const siteBadge = document.createElement("span");
    siteBadge.classList.add("badge", "badge-secondary", "ml-2");
    siteBadge.innerText = `Site ${lotNum}`;
    leftElem.appendChild(siteBadge);

    if (reservation.is_long_term) {
        const longTermBadge = document.createElement("span");
        longTermBadge.classList.add("badge", "badge-info", "ml-1");
        longTermBadge.innerText = "Long Term";
        leftElem.appendChild(longTermBadge);
    }

    const detailsElem = document.createElement("div");
    detailsElem.classList.add("text-muted", "small", "mt-1");

    const checkinSpan = document.createElement("span");
    checkinSpan.innerText = `📅 ${formatDateTime(reservation.checkin)}`;
    detailsElem.appendChild(checkinSpan);

    const arrowSpan = document.createElement("span");
    arrowSpan.classList.add("mx-1");
    arrowSpan.innerText = "→";
    detailsElem.appendChild(arrowSpan);

    const checkoutSpan = document.createElement("span");
    checkoutSpan.innerText = formatDateTime(reservation.checkout);
    detailsElem.appendChild(checkoutSpan);

    const dotSpan = document.createElement("span");
    dotSpan.classList.add("mx-2");
    dotSpan.innerText = "·";
    detailsElem.appendChild(dotSpan);

    const phoneLink = document.createElement("a");
    phoneLink.href = `tel:${reservation.phone_num}`;
    phoneLink.innerText = `📞 ${reservation.phone_num}`;
    detailsElem.appendChild(phoneLink);

    leftElem.appendChild(detailsElem);
    cardBodyElem.appendChild(leftElem);

    // Right — Actions
    const rightElem = document.createElement("div");
    rightElem.classList.add("d-flex", "mt-2");

    const viewBtn = document.createElement("a");
    viewBtn.href = `/reservations/${pk}`;
    viewBtn.classList.add("btn", "btn-sm", "btn-outline-primary", "mr-2");
    viewBtn.innerText = "View";
    rightElem.appendChild(viewBtn);

    const editBtn = document.createElement("a");
    editBtn.href = `/reservations/${pk}/edit`;
    editBtn.classList.add("btn", "btn-sm", "btn-outline-secondary", "mr-2");
    editBtn.innerText = "Edit";
    rightElem.appendChild(editBtn);

    const deleteBtn = document.createElement("a");
    deleteBtn.href = `/reservations/${pk}/delete`
    deleteBtn.classList.add("btn", "btn-sm", "btn-outline-danger");
    deleteBtn.innerText = "Delete";
    rightElem.appendChild(deleteBtn);

    cardBodyElem.appendChild(rightElem);

    return cardElem;
}

window.onload = () => {

    const csrftoken = getCookie('csrftoken');

    class ParkMap {
        constructor(mapLots) {
            this.mapLots = document.querySelectorAll("[data-site]");
            this.infoModal = document.querySelector("#site-modal");
            this.setEventListeners();
        }

        resetModal() {
            this.infoModal.querySelector("#site-modal-maintenance").classList.add("d-none");
            this.infoModal.querySelector("#site-modal-workorders").classList.add("d-none");   
            this.infoModal.querySelector("#site-modal-workorder-count").innerText = "";
            this.infoModal.querySelector("#site-modal-info").innerText = "";
            this.infoModal.querySelector(".list-group").innerHTML = "";
            this.infoModal.querySelector(".active-reservations").innerHTML = "";
        }

        setEventListeners() {
            this.mapLots.forEach(lot => {
                const siteNumber = lot.getAttribute("data-site");
                lot.addEventListener("click", async (e) => {
                    this.resetModal();
                    showLoader(".info-model-body");
                    
                    try {
                        const [site, workorders, reservations] = await Promise.all([
                            fetch(`/api/sites/${siteNumber}/`).then(res => res.json()),
                            fetch(`/api/workorders/by-lot/${siteNumber}/`).then(res => res.json()),
                            fetch(`/api/reservations/by-lot/${siteNumber}/`).then(res => res.json()),
                        ]);

                        const siteData = site[0].fields;
                        if (workorders.length > 0) {
                            this.infoModal.querySelector("#site-modal-workorders").classList.remove("d-none");
                            this.infoModal.querySelector("#site-modal-workorder-count").innerText = workorders.length;
                        }

                        if (siteData.under_maintenance) {
                            this.infoModal.querySelector("#site-modal-maintenance").classList.remove("d-none");
                        }
                        
                        const listElem = this.infoModal.querySelector(".list-group");
                        for (const [key, label] of Object.entries(amenities)) {
                            const item = siteData[key]
                                ? createListItem(label, createBadge("badge-success", "✓ Yes"), ["d-flex", "justify-content-between", "align-items-center"])
                                : createListItem(label, createBadge("badge-light", "No", ["text-muted"]), ["d-flex", "justify-content-between", "align-items-center"]);
                            listElem.appendChild(item);
                        }

                        const maxLengthText = siteData.max_length_ft ? `${siteData.max_length_ft} ft.` : "N/A";
                        const item = createListItem("Max Length", 
                            createBadge("badge-secondary", maxLengthText), 
                            ["d-flex", "justify-content-between", "align-items-center"]
                        );
                        listElem.appendChild(item);
   
                        if (reservations.length) {
                            const reservationCardList = this.infoModal.querySelector(".active-reservations");
                            for (const reservation of reservations) {
                                const cardElem = createReservationCard(reservation, siteData.lot_id);
                                reservationCardList.appendChild(cardElem);
                            }
                        }
                        
                        this.infoModal.querySelector("#site-modal-lot-id").innerText = siteData.lot_id;
                        this.infoModal.querySelector("#site-modal-lot-type").innerText = siteData.lot_type.toUpperCase();
                        this.infoModal.querySelector("#site-modal-info").innerText = siteData.info;
                        removeLoader(".info-model-body");

                    } catch (error) {
                        console.error(`Something went wrong: ${error}`);
                        removeLoader(".info-model-body");
                    } 

                });
            });

            this.infoModal.querySelector(".modal-body").addEventListener("click", (e) => {

                if (e.target.classList.contains("save")) {   
                    const updatedSiteInfoText = this.infoModal.querySelector("#site-modal-info").textContent;
                    const siteNumber = this.infoModal.querySelector("#site-modal-lot-id").innerText.trim();
                    fetch(`/api/sites/${siteNumber}/`, {
                        method: "PUT",
                        headers: {
                            "Accept": "application/json",
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrftoken
                        },
                        body: JSON.stringify({"info": updatedSiteInfoText})
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error(`Save failed: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Saved:", data);
                        this.resetModal();
                    })
                    .catch(err => {
                        console.error(err);
                    });
                }

                if (e.target.hasAttribute("data-dismiss")) {
                    this.resetModal();
                }
            });
        }

        loadOccupiedLots() {
            const today = new Date().toISOString().split('T')[0];
            fetch(`/api/reservations/on/${today}/`)
                .then(response => response.json())
                .then(data => {
                    const occupiedLots = data.map(r => ({
                        lot_id: r.site__lot_id,
                        name: r.name,
                        end: r.checkout,
                    }));
                    
                    this.mapLots.forEach(lot => {
                        // Reset Map State
                        lot.classList.remove("occupied")
                        const existingTitle = lot.querySelector("title");
                        if (existingTitle) existingTitle.remove();

                        // Set New Map State
                        const siteNum = lot.getAttribute("data-site");
                        const reservation = occupiedLots.find(r => r.lot_id === siteNum);
                        if (reservation) {
                            lot.classList.add("occupied");
                            const titleElem = document.createElementNS("http://www.w3.org/2000/svg", "title");
                            titleElem.textContent = `${reservation.name} — Checkout: ${new Date(reservation.end).toDateString()}`;
                            lot.appendChild(titleElem);
                        }
                    });
                })
                .catch(err => {
                    console.error('Failed to load occupied lots:', err);
                });
        }

        loadLotsUnderMaintenance() {
            fetch(`/api/sites/under-maintenance/`)
                .then(response => response.json())
                .then(data => {         
                    this.mapLots.forEach(lot => {
                        lot.classList.remove("maintenance")
                        
                        const siteNum = lot.getAttribute("data-site");
                        const lotUnderMaintenance = data.find(s => s.fields.lot_id === siteNum);
                        if (lotUnderMaintenance) lot.classList.add("maintenance");
                    });
                })
                .catch(err => {
                    console.error('Failed to load lots:', err);
                });
        }

    }

    const parkMap = new ParkMap();
    parkMap.loadOccupiedLots();
    parkMap.loadLotsUnderMaintenance();

    setInterval(() => {
        parkMap.loadOccupiedLots();
        parkMap.loadLotsUnderMaintenance();
    }, 600000);

    $('.checkout-form').on('submit', function(e) {
        if (!confirm('Are you sure you want to check this guest out?')) {
            e.preventDefault();
            $(this).find('button[type="submit"]')
                .prop('disabled', false)
                .text('✓ Checkout');
            return false;
        }
    });
}
