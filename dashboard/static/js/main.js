window.onload = () => {

    const state = {
        infoModalBadgeElem: null,
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

    class BadgeManager {
        static createBadge(type_of_badge, content) {
             const badgeElem = document.createElement("span");
             badgeElem.innerText = content;
             if (type_of_badge == "warning") {
                badgeElem.classList.add("badge", "badge-warning");
                return badgeElem;
             } else if (type_of_badge == "info") {
                badgeElem.classList.add("badge", "badge-warning");
                return badgeElem;
             }
        }
    }

    class Map {
        constructor(mapLots) {
            this.mapLots = document.querySelectorAll("[data-site]");
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
                            const site = data.site_info[0];
                            const total_workorders = data.workorders;
                            state.infoModalBadgeElem = BadgeManager.createBadge("warning", `${total_workorders} Uncompleted Workorder(s)`);
                            removeLoader(".info-model-body");
                            if (total_workorders > 0) {
                                this.infoModal.querySelector(".modal-header").append(state.infoModalBadgeElem);
                            }
                            this.infoModal.querySelector(".modal-title").innerText = `Site ${site.lot_id}`;
                            this.infoModal.querySelector(".content").innerText = site.info;
                            this.infoModal.querySelector(".content").setAttribute("site", site.lot_id);
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
                if (e.target.hasAttribute("data-dismiss")) {
                    if (state.infoModalBadgeElem) state.infoModalBadgeElem.remove();
                }
                if (e.target.classList.contains("save")) {
                    const siteInfoText = e.currentTarget.querySelector(".content").innerText;
                    const siteNumber = e.currentTarget.querySelector(".content").getAttribute("site");
                    const url = window.location.origin + "/site/info/" + siteNumber;
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

    const ParkMap = new Map();
    ParkMap.loadOccupiedLots();
    ParkMap.loadLotsUnderMaintenance();

    const checkinPicker = flatpickr("#checkin", {
        enableTime: true,
        dateFormat: "m/d/Y H:i",
        minuteIncrement: 30,
        allowInput: true,
        time_24hr: true,
        minDate: "today",
        onChange: function(selectedDates) {
            // When checkin changes, update checkout's minDate
            if (selectedDates.length > 0) {
                checkoutPicker.set("minDate", selectedDates[0]);
            }
        }
    });

    const checkoutPicker = flatpickr("#checkout", {
        enableTime: true,
        dateFormat: "m/d/Y H:i",
        minuteIncrement: 30,
        allowInput: true,
        time_24hr: true,
        minDate: "today",
    });

    setInterval(() => {
        ParkMap.loadOccupiedLots();
        ParkMap.loadLotsUnderMaintenance();
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
