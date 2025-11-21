// bot message template
export function botMessageTemplate(wholebotMessageId, botMessageId, sqlMessageId, actionMessageId, message_id) {
    
    // icons
    let img_links = '';
    var assistant_icon = $('#assistant_icon').val().trim();
    var white_mode = $('#white_mode').val().trim();

    if (assistant_icon == 'False') {
        if (white_mode == 'True') {
            img_links = '/static/img/white_icons/mes_icon.png';
        } else {
            img_links = '/static/img/mes_icon.png';
        }
    } else {
        img_links = `/static/${assistant_icon}`;
    }

    console.log('message_id in botMessageTemplate:', message_id);

    return `
        <div class="container mes" style="background-color: transparent;">
            <div class="d-flex justify-content-start" style="background-color: transparent;">
                <div class="div">
                    <img src="${img_links}" width="50" height="50" alt="Logo">
                </div>
                <div class="col-max-10 hovering_message" id="menu_${message_id}" style="background-color: transparent;">
                    <div id="${wholebotMessageId}" style="width: 50%;">
                        <!-- Chart or other elements go here -->
                    </div>
                    <div class="card chat_message" style="background-color: transparent;">
                        <div class="card-body" style="background-color: transparent;">
                            <div style="color: #a0a0a0; text-align: left;" id="${actionMessageId}">
                                <!-- Action Buttons will be shown here -->
                            </div>
                            <div class="format_x" id="${botMessageId}" style="background-color: transparent;">
                                <!-- Bot message will be inserted here -->
                            </div>
                            <div style="color: #a0a0a0;" id="${sqlMessageId}">
                                <!-- SQL text will be shown here -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <ul id="custom_${message_id}" class="custom-menu">
            <!-- Context menu will be generated here -->
        </ul>
    `;
}

// User message template
export function userMessageTemplate(userMessage) {
    
    // icons
    let img_links = '';
    var user_icon = $('#user_icon').val().trim();
    var white_mode = $('#white_mode').val().trim();

    if (user_icon == 'False') {
        if (white_mode == 'True') {
            img_links = '/static/img/white_icons/user_icon.png';
        } else {
            img_links = '/static/img/user_icon.png';
        }
    } else {
        img_links = `/static/${user_icon}`;
    }

    return `
        <div class="container mes">
            <div class="d-flex justify-content-end">
                <div class="col-max-7 card message user_message">
                    <div class="card-body">${userMessage}</div>
                </div>
                <div class="div">
                    <img src="${img_links}" width="50" height="50" alt="User Icon">
                </div>
            </div>
        </div>
    `;
}

// Report Modal Template
export function reportModalTemplate(view_id) {
    return `
        <div class="modal fade" id="report${view_id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Feedback</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="feedback-form">
                            <div class="card c_card">
                                <textarea class="form-control" name="feedback_${view_id}" id="feedback"></textarea>
                            </div>
                            <div class="e_card">
                                <button type="button" id="feedback-submit-btn" value="${view_id}" class="btn e_button">Submit</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Score Modal Template
export function scoreModalTemplate(view_id) {
    console.log('score_view_id:', view_id);
    return `
        <div class="modal fade" id="score${view_id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Rating</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="score-form">
                            <div class="card c_card">
                                <select id="stars_${view_id}" class="form-select dark select" aria-label="Default select example">
                                    <option value="5">5 Stars</option>
                                    <option value="4">4 Stars</option>
                                    <option value="3">3 Stars</option>
                                    <option value="2">2 Stars</option>
                                    <option value="1">1 Star</option>
                                </select>
                            </div>
                            <div class="e_card">
                                <button type="button" id="score-submit-btn" value="${view_id}" class="btn e_button">Submit</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Appendix Button Template + Custom Menu (Context Menu)
export function appendixButtonTemplate(messageId) {
    // get custom menu
    var customMenuOptions = '<li><i class="bi bi-shield-fill"></i> Safe</li>';

    // append the export charts button if visualization is activated
    var check_1 = $('#check_1').val();
    if (check_1 == 'True') {
        customMenuOptions += `<li>
                <a id="chartModalButton" type="button" data-id="${messageId}" data-bs-toggle="modal" data-bs-target="#chartExportModal">
                    <i class="bi bi-clipboard-data-fill"></i> Export Chart
                </a>
            </li>`;
    }

    // append the table export button if tables is activated
    var check_15 = $('#check_15').val();
    if (check_15 == 'True') {
        customMenuOptions +=`<li>
                <a id="tablesModalButton" type="button" data-id="${messageId}" data-bs-toggle="modal" data-bs-target="#tablesExportModal">
                    <i class="bi bi-table"></i> Export Table
                </a>
            </li>`;
    }

    customMenuOptions +=`<li>
                <a type="button" class="translate_field">
                    <i class="bi bi-translate"></i> Translate
                </a>
            </li>
            <li>
            <a type="button" data-bs-toggle="modal" data-bs-target="#score${messageId}">
                <i class="bi bi-star"></i> Score
            </a>
            </li>
            <li>
            <a type="button" data-bs-toggle="modal" data-bs-target="#report${messageId}">
                <i class="bi bi-flag"></i> Feedback
            </a>
            </li>`;

    console.log('customMenuOptions appended');
    return customMenuOptions;
}