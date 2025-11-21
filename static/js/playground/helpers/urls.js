export function handleUrlFetch(messageId, urlSpaceElement) {
    console.log('URL Offcanvas Button clicked');

    $.ajax({
        url: '/modules/web_search/urls/get',
        method: 'GET',
        data: { message_id: messageId },
        success: function (response) {
            console.log('URL-Anfrage erfolgreich:', response);
            urlSpaceElement.innerHTML = ''; // Clear previous content

            if (response.length === 0) {
                urlSpaceElement.innerHTML = `
                    <div class="card url_card">
                        No web sources found for this message.
                    </div>`;
                return;
            }

            response.forEach(function (result) {
                urlSpaceElement.insertAdjacentHTML('beforeend', `
                    <a href="${result.url}" class="card url_card">
                        ${result.title}
                    </a>`);
            });
        },
        error: function (error) {
            console.error('Fehler bei der URL-Anfrage:', error);
            urlSpaceElement.innerHTML = `
                <div class="card url_card">
                    An error occurred while fetching the URLs. Please try again later!
                </div>`;
        }
    });
}