import { userMessageTemplate, botMessageTemplate, reportModalTemplate, scoreModalTemplate, appendixButtonTemplate } from "./html_templates.js";
import { createChartElement } from "./charting.js";

// displayes the messages at the top of the page
function displaymessages(results) {
    console.log(results);

    if (results) {
        if (results.length !== 0) {

            // iterates over all messages
            results.forEach(function (result) {

                // append user messages
                if (result.role === 'user') {
                    // check for client side errors
                    try {
                        // check for server side errors
                        if (result.success) {
                            $('#messages').append(userMessageTemplate(result.content));
                        } else {
                            var error_message = '<div class="alert alert-danger" role="alert">Unfortunately, this message could not be retrieved properly. Most likely, due to an error in the initial generation of this message.</div>';
                            $('#messages').append(userMessageTemplate(marked.parse(error_message)));
                        }
                    } catch (error) {
                        console.error('Error while parsing message:', error);
                        var error_message = `<div class="alert alert-danger" role="alert">Error: ${error}. Please try again later!</div>`;
                        $('#messages').append(userMessageTemplate(marked.parse(error_message)));
                    }
                // append assistant messages
                } else {
                    // Generate unique IDs
                    const [botMessageId, wholebotMessageId, sqlMessageId, actionMessageId] = [
                        `bot_message_${result.message_id}`,
                        `wholebotmessage_${result.message_id}`,
                        `sql_message_${result.message_id}`,
                        `action_message_${result.message_id}`,
                    ];

                    // Append bot message dynamically
                    const botMessageHtml = botMessageTemplate(wholebotMessageId, botMessageId, sqlMessageId, actionMessageId, result.message_id);
                    $('#messages').append(botMessageHtml);

                    // add all content, charts and annotations
                    // check for client side errors
                    try {
                        // check for server side errors - also display if content exists even if success is false
                        if (result.success || (result.content && result.content.trim() !== '')) {
                            // add message content
                            const MessageField = document.getElementById(botMessageId);
                            MessageField.innerHTML = marked.parse(result.content.replace('【functions†source】', '').replace(/\[/g, '\\[').replace(/\]/g, '\\]'));
                            // check for mathjax formulas
                            MathJax.typesetPromise([MessageField]).catch(err => console.error(err.message));

                            // Check if MessageField contains a base64-encoded image and replace it with an error message
                            if (MessageField.innerHTML.includes("data:image/png;base64")) {
                                console.warn("Detected base64 image, replacing content with a generic message.");
                                MessageField.innerHTML = `
                                    I tried to generate a chart for you. If an error occured, please try again later!
                                `;
                            }

                            // Check Hide Appendices
                            const check_ha = $('#hide_appendix_config').val();
                            // Check Analytics
                            const check_6 = $('#check_6').val();

                            // ACTION ELEMENT
                            let act_elm = '';

                            // Fulfill Documents Citations Element
                            if (Array.isArray(result.fd_citations) && result.fd_citations.length > 0) {
                                result.fd_citations.forEach(fd => {
                                    act_elm += `
                                        <a href="/modules/fulfill_documents/export_ai?id=${fd.template_id}&fd_id=${fd.fd_citations_id}" class="btn mail_button">
                                            <i class="bi bi-pen-fill"></i> ${fd.template_name}
                                        </a>`;
                                });
                                console.log("Fd citation successfully generated");
                                MessageField.innerHTML = MessageField.innerHTML.replace(
                                    /sandbox\s*:\/\/\s*([^) \n]+)/gi,
                                    `/modules/fulfill_documents/export_ai?id=${result.fd_citations[0].template_id}&m_id=${result.message_id}`
                                );
                            } else {
                                console.log("No fd citation data available.");
                            }

                            // Mail Element
                            if (Array.isArray(result.mail) && result.mail.length > 0) {
                                result.mail.forEach(m => {
                                    act_elm += `
                                        <a href="${m.link}" class="btn mail_button">
                                            <i class="bi bi-envelope"></i> ${m.subject}
                                        </a>`;
                                });
                                console.log("Mail link successfully generated");
                            } else {
                                console.log("No mail data available.");
                            }

                            // add hr for functions
                            if (result.fd_citations.length > 0 || result.mail.length > 0) {
                                act_elm += '<hr>';
                            }

                            document.getElementById(actionMessageId).innerHTML = act_elm;

                            // CITATION ELEMENT
                            let cit_elm = '';
        
                            // SQL Text
                            console.log("SQL Answer: ", result.sql);
                            if (check_6 == 'True' && check_ha === 'False') {
                                if (result.sql !== '') {
                                    cit_elm += '<hr>';
                                    cit_elm += `
                                        <h class="sql_text">${result.sql}</h>`;
                                    console.log("SQL successfully generated");
                                } else {
                                    console.log("No SQL data available.");
                                }
                            }

                            // hide appendices
                            if (check_ha === 'False') {
                                // add hr for sources
                                if (result.annotations.length > 0 || result.url_indicator !== '' || result.database !== '' || result.api_citations.length > 0) {
                                    cit_elm += '<hr>';
                                }

                                // Database Element
                                if (result.database !== '') {
                                    cit_elm += `
                                        <a type="button" class="btn preview_button" disabled>
                                            <i class="bi bi-database-fill"></i> ${result.database}
                                        </a>`;
                                    cit_elm += '<br>';
                                    console.log("Database citation successfully generated");
                                } else {
                                    console.log("No database data available.");
                                }

                                // Citation Element
                                if (Array.isArray(result.annotations) && result.annotations.length > 0) {
                                    result.annotations.forEach(anno => {
                                        cit_elm += `
                                            <a id="fetchfile" data-file-id="${anno.id}" data-bs-toggle="offcanvas" data-bs-target="#preview_offcanvas" type="button" class="btn preview_button fetchfile">
                                                <i class="bi bi-file-earmark-text-fill"></i> ${anno.title}
                                            </a>`; // temporary without indices
                                        cit_elm += '<br>';
                                    });
                                    console.log("Citations successfully generated");
                                } else {
                                    console.log("No citation data available.");
                                }

                                // URL Element
                                if (result.url_indicator !== '') {
                                    cit_elm += `
                                        <a id="fetchurl" data-message-id="${result.message_id}" data-bs-toggle="offcanvas" data-bs-target="#url_offcanvas" type="button" class="btn preview_button">
                                            <i class="bi bi-globe-americas" style="margin-right: 10px;"></i> ${result.url_indicator}
                                        </a>`;
                                    cit_elm += '<br>';
                                    console.log("URL indicator successfully generated");
                                } else {
                                    console.log("No url data available.");
                                }

                                // API Element
                                if (result.api_citations.length > 0) {
                                    result.api_citations.forEach(api => {
                                        cit_elm += `
                                            <a class="btn preview_button" disabled>
                                                <i class="bi bi-hdd-network-fill"></i> ${api}
                                            </a>`;
                                    });
                                    console.log("API citation successfully generated");
                                }
                            }

                            document.getElementById(sqlMessageId).innerHTML = cit_elm;
                            // add message charts
                            // Create charts if available
                            if (Array.isArray(result.charts) && result.charts.length > 0) {
                                createChartElement(result.charts, result.chart_ids, document.getElementById(wholebotMessageId));
                            }
                            // add score and feedback modals and buttons
                            $('#modals').append(reportModalTemplate(result.message_id), scoreModalTemplate(result.message_id));
                            document.getElementById(`custom_${result.message_id}`).innerHTML = appendixButtonTemplate(result.message_id);
                        } else {
                            var error_message = '<div class="alert alert-info" role="alert">It seems you may have left the chat before the message generation was completed. Please refresh the page to view the result.</div>';
                            document.getElementById(botMessageId).innerHTML = error_message;  
                        }
                    } catch (error) {
                        console.error('Error while parsing message:', error);
                        var error_message = `<div class="alert alert-danger" role="alert">Error: ${error}. Please try again later!</div>`;
                        document.getElementById(botMessageId).innerHTML = error_message;  
                    } 
                }
            });
            // scroll to bottom
            window.scrollTo(0, document.body.scrollHeight); 
            // activate tooltips
            $('[data-bs-toggle="tooltip"]').tooltip();
        }
    }
};

// gets the messages of this chat
export function initializeMessages() {
    const thread_id = $('#current_thread_id').val();
    $.ajax({
        url: '/playground/messages/get',
        method: 'GET',
        data: { thread_id: thread_id },
        success: function (response) {
            console.log('AJAX-Anfrage erfolgreich:', response);
            displaymessages(response);
        },
        error: function (error) {
            console.error('Fehler bei der AJAX-Anfrage:', error);
        }
    });
}