$(document).ready(function() {

    function selectSite(siteId) {
        const checkin = $('#sites-data').data('checkin');
        const checkout = $('#sites-data').data('checkout');

        $('[name="site"]').val(siteId);
        $('[name="checkout"]').val(checkout);
        $('[name="checkin"]').val(checkin);
    };

    $('.site-list-item').each(function(index, element) {
        $(element).on('click', function() {
            const siteId = $(this).data('pk');
            selectSite(siteId);
        });
    });

    const $sites = $('polygon[data-site], path[data-site]');
    $sites.on('click', function() {
        const siteNum = $(this).data('site');
        const $card = $(`.card[data-site="${siteNum}"]`);
        const siteId = $card.data('pk');
        selectSite(siteId);

        $card[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        $card.addClass('card-flash');
        setTimeout(function() {
            $card.removeClass('card-flash');
            $('#customer-form-modal').modal('show');
        }, 600);
    });

    const sites = JSON.parse($('#sites-data').text());
    for (let siteNum of sites) {
        const $site = $(`[data-site="${siteNum}"]`);
        if ($site.length) {
            $site.addClass("available");
        } else {
            console.warn(`Site ${siteNum} not found on map.`);
        }
    }
});