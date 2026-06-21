window.onload = () => {
    const lotNodes = document.querySelectorAll("[data-site]");
    const occupiedLots = JSON.parse(document.getElementById("occupied-lots-data").textContent);

    const state = {
        activeSiteId: null,
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
            this.mapLots = mapLots;
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

        highlightLots() {
            this.mapLots.forEach(lot => {
                const siteNum = lot.getAttribute("data-site");
                const reservation = occupiedLots.find(r => r.lot_id === siteNum);
                if (reservation) {
                    lot.setAttribute("id", "active");
                    const titleElem = document.createElementNS("http://www.w3.org/2000/svg", "title");
                    titleElem.textContent = `${reservation.name} — Checkout: ${new Date(reservation.end).toDateString()}`;
                    lot.appendChild(titleElem);
                }
            })
        }
    }

    const NewMap = new Map(lotNodes);
    NewMap.highlightLots();
}
